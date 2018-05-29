import os
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from users.models import UserProfile
from .models import Attivita, Image, Tipologia, get_upload_path
from recensioni.models import Recensione
from .forms import AttivitaForm, UploadImageForm, TipologieForm
from recensioni.forms import RecensioneForm
from Custom.TipologieUtils import add_tipe_object
from Custom.Utilities import get_consigliati
from Custom.AddAttivitaUtils import update_coordinates_from_address, add_attivita


# Create your views here.
def index(request):
    """Genera i contenuti della homepage del sito e renderizza il template
    :param request: richiesta HTTP della pagina
    :return: Template renderizzato con il context generato
    """
    context = dict()
    context['top_attivita_list'] = Attivita.objects.order_by('-reputazione')[:5]
    context['top_user_list'] = UserProfile.objects.order_by('-affidabilita')[:5]
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None

        if profile:
            context['consigliati'] = get_consigliati(request)

    return render(request, 'attivita/index.html', context)


class AttView(generic.DetailView):
    """Generic view della pagina dettaglio di una singola attività"""
    model = Attivita
    template_name = 'attivita/detail.html'

    def get_context_data(self, **kwargs):
        """Calcola e ritorna il context da passare al template"""
        context = super().get_context_data(**kwargs)
        context['recensioni'] = Recensione.objects.filter(attivita=self.object).order_by('-data')
        return context


@permission_required('recensioni.add_recensione')
def recensisci(request, pk):
    """Gestisce la richiesta di recensire un'attività

    Se richiesta GET, mostra il form da compilare, se richiesta POST controlla
    la correttezza del form e se sbagliato ricarica la pagina notificando gli
    errori, se giusto crea la recensione e reindirizza alla pagina dell'attività

    :param request: richiesta HTTP della pagina
    :param pk: id attività da recensire
    :return: Template renderizzato con il context generato
    """
    attivita = get_object_or_404(Attivita, pk=pk)
    if request.user in [r.autore.user for r in attivita.recensione_set.all()]:
        messages.error(request, "Hai già recensito questa attività")
        return HttpResponseRedirect(reverse('attivita:detail', args=(attivita.id,)))

    if request.method == 'GET':
        form = RecensioneForm()
        return render(request, 'attivita/recensisci.html', {'form': form, 'pk': pk})
    else:  # richiesta POST
        # Salvataggio recensione (uso form bound)
        form = RecensioneForm(request.POST)
        if form.is_valid():
            data = timezone.now().date()
            attivita.recensione_set.create(attivita=attivita, autore=request.user.user_profile,
                                           data=data,
                                           voto=form.cleaned_data.get('voto'),
                                           testo=form.cleaned_data.get('testo'))
            attivita.update_reputazione()
            attivita.update_tagcloud()
            messages.success(request, "Attività recensita, grazie della tua recensione!")
            return HttpResponseRedirect(reverse('attivita:detail', args=(pk,)))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'attivita/recensisci.html', {'form': form, 'pk': pk})


@permission_required('attivita.change_attivita')
def modify(request, pk):
    """Gestisce la richiesta di modifica di un'attività

    Se richiesta GET, mostra il form di modifica, se richiesta POST, controlla
    validità del form e salva le nuove informazioni nel DB.

    :param request: richiesta HTTP
    :param pk: id attività da modificare
    :return: Template renderizzato con il context generato
    """
    att = get_object_or_404(Attivita, pk=pk)
    if request.user != att.proprietario.user:
        return HttpResponseForbidden("L'utente loggato non può modificare l'attività")

    if request.method == 'POST':
        if 'attivitainfo' in request.POST:
            form = AttivitaForm(request.POST, instance=att)
            if form.is_valid():
                new_att = form.save()
                update_coordinates_from_address(new_att)
                messages.success(request, "Attività modificata")
                return HttpResponseRedirect(reverse('attivita:modify', args=(pk,)))
            else:
                messages.error(request, "Errore nella compilazione del form")
                return render(request, 'attivita/modifica.html', {'form': form, 'pk': pk})
        elif 'tipologieinfo' in request.POST:
            form = TipologieForm(request.POST)
            if form.is_valid():
                if form.has_changed():
                    add_tipe_object(att, form)
                    messages.success(request, "Tipologie attività aggiornate")
                return HttpResponseRedirect(reverse('attivita:modify', args=(att.id,)))
            else:
                messages.error(request, "Errore nella compilazione del form")
                return render(request, 'attivita/modifica.html', {'form': form, 'pk': pk})
    else:
        attform = AttivitaForm(att.__dict__)
        # Inizializzo checkbox tipologie
        data = {}
        for t in Tipologia.objects.all():
            data[t.nome] = (t in att.tipologie.all())
        tipform = TipologieForm(data)
        return render(request, 'attivita/modifica.html', {'attform': attform,
                                                          'tipform': tipform,
                                                          'pk': pk,
                                                          'attivita': att})


@permission_required('attivita.add_attivita')
def add(request):
    """Gestisce la richiesta di aggiunta di un'attività.

    Se richiesta GET, mostra il form di aggiunta informazioni e tipologie, se
    richiesta POST controlla la correttezza dei form e crea nuova attività.

    :param request: richiesta HTTP
    :return: Template renderizzato con il context generato
    """
    if request.method == 'POST':
        attform = AttivitaForm(request.POST, prefix='attivita')
        tipform = TipologieForm(request.POST, prefix='tipologie')
        if attform.is_valid() and tipform.is_valid() and request.user.owner_profile:
            att = add_attivita(attform, request.user.owner_profile, tipform)
            if att:
                messages.success(request, "Attività aggiunta con successo")
                return HttpResponseRedirect(reverse('attivita:detail', args=(att.id,)))
            else:
                messages.error(request, "Qualcosa è andato storto :(")
                return HttpResponseBadRequest('Qualcosa è andato storto :(')
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'attivita/add.html', {'attform': attform, 'tipform': tipform})
    else:
        attform = AttivitaForm(prefix='attivita')
        tipform = TipologieForm(prefix='tipologie')
        return render(request, 'attivita/add.html', {'attform': attform, 'tipform': tipform})


@permission_required('attivita.change_attivita')
def add_image(request, pk):
    """Gestisce aggiunta immagine

    :param request: richiesta HTTP
    :param pk: id attività di cui aggiungere l'immagine
    :return: Template renderizzato con il context generato
    """
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.attivita = get_object_or_404(Attivita, pk=pk)
            img.filename = os.path.split(get_upload_path(img, None))[-1]
            img.save()
            messages.success(request, "Immagine aggiunta all'attività")
            return HttpResponseRedirect(reverse('attivita:modify', args=(pk,)))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'attivita/upload_image.html', {'pk': pk, 'form': form})
    else:
        form = UploadImageForm()
        return render(request, 'attivita/upload_image.html', {'pk': pk, 'form': form})


@permission_required('attivita.change_attivita')
def delete_image(request, pk):
    """Gestisce eliminazione immagine

    :param request: richiesta HTTP
    :param pk: id immagine da eliminare
    :return: redirezione alla pagina di modifica attività
    """
    img = get_object_or_404(Image, pk=pk)
    img.delete()
    messages.success(request, "Immagine rimossa")
    return HttpResponseRedirect(reverse('attivita:modify', args=(img.attivita.id,)))
