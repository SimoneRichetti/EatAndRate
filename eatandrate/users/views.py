from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from notifications.models import Notification, Answer
from .forms import UserRegistrationForm, UserModifyForm
from users.models import UserProfile, OwnerProfile
from attivita.forms import AttivitaForm, TipologieForm
from Custom.AddAttivitaUtils import add_attivita


# Create your views here.
@login_required()
def my_profile(request):
    """Renderizza pagina "Il mio profilo"

    Data la richiesta con utente autenticato, viene il recuperato il profilo
    (utente o proprietario) con relative notifiche. Dopodichè, viene
    renderizzato il relativo template

    :param request: richiesta HTTP
    :return: Template renderizzato con relativo context
    """
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden("Impossibile accedere a pagina profilo")

    context = {'utente': user}
    try:
        owner = OwnerProfile.objects.get(user=user)
    except OwnerProfile.DoesNotExist:
        owner = None

    if owner:
        # build notification set
        notifiche = Notification.objects.filter(destinatario=owner, visualizzata=False)
        context['notifiche'] = notifiche
        return render(request, 'users/my_owner_profile.html', context=context)
    else:
        # build notification set
        risposte = Answer.objects.filter(notifica__mittente=user.user_profile, visualizzata=False)
        context['risposte'] = risposte
        return render(request, 'users/my_profile.html', context=context)


def user_profile(request, pk):
    """Renderizza pagina del profilo di un utente

    :param request: richiesta HTTP
    :param pk: chiave utente
    :return: Template renderizzato con relativo context
    """
    user = User.objects.get(pk=pk)

    if not user.is_active:
        messages.info(request, "L'utente è stato cancellato")
        return HttpResponseRedirect(reverse('attivita:index'))

    if request.user == user:
        return HttpResponseRedirect(reverse('users:my_profile'))

    context = {'utente': user}
    try:
        owner = OwnerProfile.objects.get(user=user)
    except OwnerProfile.DoesNotExist:
        owner = None

    if owner:
        return render(request, 'users/owner_page.html', context=context)
    else:
        return render(request, 'users/profile_page.html', context=context)


def register(request):
    """Registra un nuovo utente

    Se richesta GET, mostra form per inserire informazioni, se POST esegue
    controllo di validità sul form, crea utente e profilo e assegna tutti i
    permessi relativi alle recensioni

    :param request: richiesta HTTP
    :return: Template renderizzato o redirezione a pagina del profilo
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            userprofile = UserProfile(user=user)
            userprofile.save()

            content_type = ContentType.objects.get(model='recensione')
            permission1 = Permission.objects.get(content_type=content_type,
                                                 codename='add_recensione')
            permission2 = Permission.objects.get(content_type=content_type, codename='can_vote_review')
            permission3 = Permission.objects.get(content_type=content_type,
                                                 codename='delete_recensione')
            permission4 = Permission.objects.get(content_type=content_type,
                                                 codename='change_recensione')

            user.user_permissions.add(permission1, permission2, permission3, permission4)
            login(request, user)
            messages.success(request, 'Utente registrato con successo!')
            return HttpResponseRedirect(reverse('users:my_profile'))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})


def register_owner(request):
    """Registra un nuovo proprietario e la relativa attività

    Se richiesta GET, mostra form per inserire informazioni proprietario,
    informazioni attività e relative tipologie, se richiesta POST controlla
    la validità dei form, crea nuovo utente e relativo profilo proprietario,
    crea l'attività e la associa alle tipologie selezionate.

    :param request: richiesta HTTP
    :return: redirezione alla pagina del profilo o renderizza template registrazione
    """
    if request.method == 'POST':
        uf = UserRegistrationForm(request.POST, prefix='user')
        af = AttivitaForm(request.POST, prefix='attivita')
        tf = TipologieForm(request.POST, prefix='tipologie')
        if uf.is_valid() and af.is_valid() and tf.is_valid():
            uf.save()
            username = uf.cleaned_data.get('username')
            raw_password = uf.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            op = OwnerProfile(user=user)
            op.save()
            add_attivita(af, op, tf)

            content_type = ContentType.objects.get(model='attivita')
            permission1 = Permission.objects.get(content_type=content_type,
                                                 codename='add_attivita')
            permission2 = Permission.objects.get(content_type=content_type,
                                                 codename='delete_attivita')
            permission3 = Permission.objects.get(content_type=content_type,
                                                 codename='change_attivita')
            user.user_permissions.add(permission1, permission2, permission3)
            login(request, user)
            messages.success(request, 'Proprietario e attività registrati con successo!')
            return HttpResponseRedirect(reverse('users:my_profile'))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'users/register_owner.html', {'uf': uf, 'af': af, 'tf': tf,
                                                                 'error_msg': 'Invalid form'})
    else:
        uf = UserRegistrationForm(prefix='user')
        af = AttivitaForm(prefix='attivita')
        tf = TipologieForm(prefix='tipologie')
        return render(request, 'users/register_owner.html', {'uf': uf, 'af': af, 'tf': tf})


def modify_profile(request):
    """Gestisce modifica dei dati di un utente

    Se richiesta GET mostra form di modifica, se richiesta POST controlla i
    form e salva modifiche nel DB.

    :param request: richiesta HTTP
    :return: renderizza template o redireziona a pagina del profilo
    """
    if request.method == 'POST':
        form = UserModifyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilo modificato con successo")
            return HttpResponseRedirect(reverse('users:my_profile'))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return render(request, 'users/modify_profile.html', {'form': form})
    else:
        form = UserModifyForm(instance=request.user)
        return render(request, 'users/modify_profile.html', {'form': form})


def delete_profile(request):
    """Elimina utente

    Non avviene la cancellazione dell'utente del DB per preservare le relative
    recensioni o attività, ma viene settato il flag `is_active` a False, in
    modo che non possa più loggarsi.

    :param request: richiesta HTTP
    :return: redirezione alla homepage
    """
    if request.user.is_authenticated:
        request.user.is_active = False
        request.user.save()
        logout(request)
        messages.success(request, "Profilo eliminato")
    else:
        messages.error(request, "Errore: non sei loggato!")

    return HttpResponseRedirect(reverse('attivita:index'))
