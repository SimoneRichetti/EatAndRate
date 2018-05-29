from django.dispatch import receiver

from notifications.models import Notification
from django.db.models.signals import post_save
from recensioni.models import Recensione


@receiver(post_save, sender=Recensione)
def send_notification(sender, instance, **kwargs):
    """Dopo la creazione di una recensione invia notifica al proprietario attività

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    Notification.objects.create(mittente=instance.autore,
                                destinatario=instance.attivita.proprietario,
                                recensione=instance)
