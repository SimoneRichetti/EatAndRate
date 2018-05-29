from django.db import models
from django.utils import timezone
import datetime

from attivita.models import Attivita
from users.models import UserProfile


# Create your models here.
class Recensione(models.Model):
    """Definisce una recensione

    Attributi:
        attivita (ForeignKey): attività recensita
        autore (ForeignKey)
        data (DateField)
        voto (IntegerField): voto recensione da 1 a 5
        testo (TextField)
        utilita (IntegerField): voti ricevuti dalla recensione da altri utenti
        votanti (ManyToManyField): utenti che hanno valutato la recensione
    """
    attivita = models.ForeignKey(Attivita, on_delete=models.CASCADE)
    autore = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    data = models.DateField('Data di pubblicazione', default=datetime.date.today)
    voto = models.IntegerField('Voto', default=3, choices=[(i, str(i)) for i in range(1, 6)])
    testo = models.TextField('Testo Recensione', max_length=1000)
    utilita = models.IntegerField(default=0)
    votanti = models.ManyToManyField(UserProfile, related_name='votanti', blank=True)

    def __str__(self):
        """Definisce la stringa per identificare la recensione

        :return: stringa recensione
        :rtype str
        """
        return str(self.autore.user.username + " on " + self.attivita.nome)

    def save(self, *args, **kwargs):
        """Aggiunge un controllo prima del salvataggio nel DB

        Se il voto non è compreso tra 1 e 5 o la data è una data futura,
        viene sollevato un `ValueError`

        Params:
            :param args: lista variabile di argomenti da passare al metodo save di django
            :param kwargs: dictionary variabile di argomenti da passare al metodo
                save di django
            :return:
        """
        if self.voto < 1 or self.voto > 5:
            raise ValueError("Wrong value for field 'voto'")
        elif self.data > timezone.now().date():
            raise ValueError("Wrong value for field 'data'")
        elif self.testo == '':
            raise ValueError("'testo' field is required")
        else:
            super(Recensione, self).save(*args, **kwargs)

    class Meta:
        """Crea permesso per votare la recensione"""
        permissions = (
            ('can_vote_review', 'Can Vote Review'),
        )
