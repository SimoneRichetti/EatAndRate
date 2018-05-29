from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from notifications.forms import AnswerForm
from notifications.models import Notification, Answer


# Create your views here.
def reply(request, pk):
    """Gestisce la risposta ad una notifica

    Se richiesta GET, mostra form di risposta, se richiesta POST, check sul
    form e invia risposta

    :param request: richiesta HTTP
    :param pk: id notifica
    :return: redirezione a pagina del profilo o mostra form risposta
    """
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            notifica = get_object_or_404(Notification, pk=pk)
            answer.notifica = notifica
            answer.save()
            notifica.visualizzata = True
            notifica.save()
            messages.success(request, "Risposta inviata")
            return HttpResponseRedirect(reverse('users:my_profile'))
        else:
            messages.error(request, "Errore nella compilazione del form")
            return HttpResponseRedirect(request.path)
    else:
        form = AnswerForm()
        return render(request, 'notifications/reply.html', {'form': form, 'pk': pk})


def delete(request, pk, is_answer):
    """Cancella notifica/risposta

    Viene settato il flag `visualizzata` della notifica o della risposta a True,
    così che non venga più mostrata

    :param request: richiesta HTTP
    :param pk: id notifica/risposta
    :param is_answer: indica se di vuole cancellare una risposta
    :return: redirezione alla pagina del profilo
    """
    if is_answer:
        notifica = get_object_or_404(Answer, pk=pk)
    else:
        notifica = get_object_or_404(Notification, pk=pk)

    notifica.visualizzata = True
    notifica.save()
    return HttpResponseRedirect(reverse('users:my_profile'))


def delete_notification(request, pk):
    """Cancella notifica

    Vedi `delete(request, pk, is_answer)`

    :param request: richiesta HTTP
    :param pk: id notifica
    :return:
    """
    return delete(request, pk, False)


def delete_answer(request, pk):
    """Cancella risposta

    Vedi `delete(request, pk, is_answer)`

    :param request: richiesta HTTP
    :param pk: id risposta
    :return:
    """
    return delete(request, pk, True)
