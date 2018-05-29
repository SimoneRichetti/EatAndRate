from django.contrib import messages
from django.forms import Form
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from Custom.TipologieUtils import add_tipe_object
from attivita.forms import TipologieForm
from search.forms import RicercaComplessaForm
from .models import RicercaSemplice, RicercaComplessa
from attivita.models import Attivita


# Create your views here.
def simple_search(request):
    """Controlla form e crea ricerca semplice

    Controlla che il contenuto del form sia valido e in caso affermativo redirige
    alla pagina dei risultati, se no invoca una BadRequest

    :param request: richiesta HTTP
    :return: redirezione o HttpResponseBadRequest
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Impossibile fare richiesta GET su simple_search view')
    elif request.POST['testo_ricerca'] == '':
        return HttpResponseRedirect(reverse('attivita:index'))

    form = Form(request.POST)
    if form.is_valid():
        if request.POST['testo_ricerca'] != '':
            ricerca = RicercaSemplice(testo=request.POST['testo_ricerca'])
            ricerca.save()
            return HttpResponseRedirect(reverse('search:simple_results', args=(ricerca.id,)))

    print('Qualcosa è andato storto')
    messages.error(request, "Errore nella compilazione form")
    return HttpResponseRedirect(reverse('attivita:index'))


def complex_search(request):
    """Controlla form e crea ricerca complessa

    Controlla che il contenuto dei form sia valido e in caso affermativo redirige alla
    pagina dei risultati, se no invoca mostra errore e redirige a homepage

    :param request: richiesta HTTP
    :return: risposta HTTP
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Impossibile fare richiesta GET su complex_search view')

    rcf = RicercaComplessaForm(request.POST, prefix='search_info')
    tf = TipologieForm(request.POST, prefix='search_tipologie')
    if rcf.is_valid() and tf.is_valid():
        ricerca = rcf.save()
        add_tipe_object(ricerca, tf)
        return HttpResponseRedirect(reverse('search:complex_results', args=(ricerca.id,)))
    else:
        messages.error(request, "Errore nella compilazione form")
        return HttpResponseRedirect(reverse('attivita:index'))


def show_results(request, results):
    """Mostra risultati della ricerca e mappa con marker per ogni risultato

    :param request: richesta HTTP
    :param results: iterabile contenente i risultati
    :return: Template renderizzato con relativo context
    """
    rcf = RicercaComplessaForm(prefix='search_info')
    tf = TipologieForm(prefix='search_tipologie')
    if not results:
        return render(request, 'search/results.html', {'error_msg': 'Nessun risultato di ricerca',
                                                       'rcf': rcf,
                                                       'tf': tf})
    else:
        results = results[:20]
        for r in results:
            first_result = r
            if r.latitudine and r.longitudine:
                return render(request, 'search/results.html', {'results': results,
                                                               'rcf': rcf,
                                                               'tf': tf,
                                                               'first_result': first_result})
        return render(request, 'search/results.html', {'results': results,
                                                       'rcf': rcf,
                                                       'tf': tf})


def simple_results(request, pk):
    """Calcola risultati di una ricerca semplice

    Si crea una lista contenente tutte le attività che contengo la stringa ricercata
    nel nome, nell'indirizzo o nella città

    :param request: richiesta HTTP
    :param pk: id ricerca
    :return:
    """
    ricerca = get_object_or_404(RicercaSemplice, pk=pk)
    text = ricerca.testo.lower()
    results = list()

    for att in Attivita.objects.order_by('-reputazione'):
        if (text in att.nome.lower()) or (text in att.citta.lower()) \
                or (text in att.descrizione.lower()):
            results.append(att)

    return show_results(request, results)


def complex_results(request, pk):
    """Calcola risultati di una ricerca complessa

    Viene creata una lista contenente tutte le attività che rispettano i filtri
    su nome, città e tipologie contenuti nella ricerca e vengono passati alla
    view `show_results`

    :param request: richiesta HTTP
    :param pk: id ricerca
    :return:
    """
    ricerca = get_object_or_404(RicercaComplessa, pk=pk)
    results = list(Attivita.objects.order_by('-reputazione'))

    # check Nome
    if ricerca.testo_nome != '':
        print('Valuto campo nome')
        results = list()
        pattern = ricerca.testo_nome.lower()
        for attivita in Attivita.objects.order_by('-reputazione'):
            if pattern in attivita.nome.lower():
                results.append(attivita)
        del pattern
        print('Post-nome:', results)

    # check Città
    if ricerca.testo_citta != '':
        print('Valuto città')
        results_nome = results
        results = list()
        pattern = ricerca.testo_citta.lower()
        for attivita in results_nome:
            if pattern in attivita.citta.lower():
                results.append(attivita)
        del results_nome
        del pattern
        print('Post città:', results)

    # check Tipologie
    if ricerca.tipologie.count() > 0:
        for tipo in ricerca.tipologie.all():
            previous_results = results
            results = list()
            for att in previous_results:
                if tipo in att.tipologie.all():
                    results.append(att)

    # ricerca.delete()
    return show_results(request, results)
