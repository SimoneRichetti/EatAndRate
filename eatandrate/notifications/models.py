"""Definisce i modelli per l'app `notifications`

Modelli:
    Notification
    Answer
"""
from django.db import models

from recensioni.models import Recensione
from users.models import UserProfile, OwnerProfile


# Create your models here.
class Notification(models.Model):
    """Definisce una notifica

    Attributi:
        mittente (ForeignKey)
        destinatario (ForeignKey)
        recensione (ForeignKey)
        visualizzata (BooleanField): booleano che indica se la notifica sia
            stata visualizzata dal destinatario o meno
    """
    mittente = models.ForeignKey(UserProfile, verbose_name='mittente',
                                 on_delete=models.CASCADE)
    destinatario = models.ForeignKey(OwnerProfile, verbose_name='destinatario',
                                     on_delete=models.CASCADE)
    recensione = models.ForeignKey(Recensione, verbose_name='recensione',
                                   on_delete=models.CASCADE)
    visualizzata = models.BooleanField(default=False)

    def __str__(self):
        """Definisce la stringa per identificare la notifica

        :return: stringa tipologia
        :rtype str
        """
        return self.mittente.user.username + ' to ' + self.destinatario.user.username


class Answer(models.Model):
    """Definisce la risposta ad una notifica

    Attributi:
        notifica (ForeignKey): notifica di cui è risposta
        riposta (TextField): testo risposta
        visualizzata (BooleanField)
    """
    notifica = models.ForeignKey(Notification, verbose_name='notifica originale',
                                 on_delete=models.CASCADE)
    risposta = models.TextField('risposta', max_length=256)
    visualizzata = models.BooleanField(default=False)

    def __str__(self):
        """Definisce la stringa per identificare la risposta

        :return: stringa risposta
        :rtype str
        """
        return 'answer of' + self.notifica.__str__()
