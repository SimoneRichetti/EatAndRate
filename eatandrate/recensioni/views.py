from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from recensioni.models import Recensione


# Create your views here.
@permission_required('recensioni.can_vote_review')  # probabilmente inutile perchè chiamato da funzioni
# su cui viene già effettuato un controllo, ma più sicuro
def vote(request, pk, is_vote_positive):
    """Aggiunge un voto positivo o negativo ad una recensione

    Dopo aver controllato che l'utente che effettua la richiesta non sia l'autore
    della recensione o non la abbia già valutata, modifica l'utilità della recensione
    a seconda del giudizio espresso dall'utente

    :param request: richiesta HTTP
    :param pk: chiave primaria recensione
    :param is_vote_positive: indica se il giudizio è positivo o negativo
    :return: redirezione alla pagina dell'attività
    """
    rec = get_object_or_404(Recensione, pk=pk)
    if request.user == rec.autore.user:
        messages.error(request, "Non puoi votare le tue recensioni")
    elif request.user.user_profile in rec.votanti.all():
        messages.error(request, "Hai già votato questa recensione!")
    else:
        inc = 1
        if not is_vote_positive:
            inc *= -1
        rec.utilita += inc
        if is_vote_positive or rec.autore.affidabilita > 0:  # Impedisco che affidabità diventi negativo
            rec.autore.affidabilita += inc
        rec.votanti.add(request.user.user_profile)
        rec.save()
        rec.autore.save()
        rec.attivita.update_reputazione()
        messages.success(request, "Recensione votata!")
    return HttpResponseRedirect(reverse('attivita:detail', args=(rec.attivita.id,)))


@permission_required('recensioni.can_vote_review')
def vote_pos(request, pk):
    """Valuta positivamente una recensione

    :param request: richiesta HTTP
    :param pk: chiave recensione
    :return:
    """
    return vote(request, pk, True)


@permission_required('recensioni.can_vote_review')
def vote_neg(request, pk):
    """Valuta negativamente una recensione

    :param request: richiesta HTTP
    :param pk: chiave recensione
    :return:
    """
    return vote(request, pk, False)
