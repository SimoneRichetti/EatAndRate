from django.http import HttpResponseRedirect
from django.urls import reverse


def welcome(request):
    """Reindirizza all'index url del sito

    :param request: richiesta HTTP
    :return: risposta HTTP con reindirizzamento
    """
    return HttpResponseRedirect(reverse('attivita:index'))
