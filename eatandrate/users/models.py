from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    """Definisce il profilo di un utente registrato

    Attributi:
        user (OneToOneField): django user relativo al profilo
        affidabilita (PositiveIntegerField): punteggio di affidabilità dell'utente
            dato dalle valutazioni delle sue recensioni

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    affidabilita = models.PositiveIntegerField(default=25)

    def __str__(self):
        """Definisce la stringa per identificare il profilo utente

        :return: stringa profilo utente
        :rtype str
        """
        return self.user.username


class OwnerProfile(models.Model):
    """Definisce il profilo di un proprietario di attività

    Attributi:
        user (OneToOneField): django user relativo al profilo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')

    def __str__(self):
        """Definisce la stringa per identificare il profilo proprietario

        :return: stringa profilo proprietario
        :rtype str
        """
        return self.user.username
