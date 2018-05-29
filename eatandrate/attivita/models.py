"""Definisce i modelli per l'app `attivita`

Modelli:
    Tipologia
    Attività
    Immagine

Funzioni:
    get_upload_path
"""
import os

from users.models import OwnerProfile
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from eatandrate.settings import BASE_DIR
from Custom.Utilities import create_tag_cloud


# Create your models here.
class Tipologia(models.Model):
    """Definisce una tipologia attribuibile ad un'attività

    Attributi:
        nome (CharField): nome della tipologia
    """
    nome = models.CharField('nome', max_length=25, unique=True, default='Useless Tipology')

    def __str__(self):
        """Definisce la stringa per identificare la tipologia

        :return: stringa tipologia
        :rtype str
        """
        return self.nome


class Attivita(models.Model):
    """Definisce un'attività

    Attributi:
        nome (CharField)
        indirizzo (CharField)
        citta (CharField)
        reputazione (FloatField): punteggio dell'attività basato sulle
            recensioni ricevute
        descrizione (TextField)
        proprietario (ForeignKey): chiave esterna al profilo di un proprietario
        tipologie (ManyToManyField): riferimento alle tipologie dell'attività
        latitudine (FloatField)
        longitudine (FloatField)
    :return
    """
    nome = models.CharField('Nome', max_length=50)
    indirizzo = models.CharField('Indirizzo', max_length=50)
    citta = models.CharField('Città', max_length=30)
    reputazione = models.FloatField('Reputazione', default=0,
                                    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    descrizione = models.TextField('Descrizione', blank=True,
                                   max_length=500)
    proprietario = models.ForeignKey(OwnerProfile, on_delete=models.CASCADE, null=True)
    tipologie = models.ManyToManyField(Tipologia, blank=True)
    latitudine = models.FloatField('Latitudine', blank=True, null=True)
    longitudine = models.FloatField('Longitudine', blank=True, null=True)

    def __str__(self):
        """Definisce la stringa per identificare l'attività

        :return: stringa attività
        :rtype str
        """
        return self.nome

    def save(self, *args, **kwargs):
        """Aggiunge un controllo sulla reputazione prima del salvataggio nel DB

        In caso il controllo fallisca, viene sollevato un `ValueError`

        Params:
            :param args: lista variabile di argomenti da passare al metodo save di django
            :param kwargs: dictionary variabile di argomenti da passare al metodo
                save di django
            :return:
        """
        if 0. <= self.reputazione <= 5.:
            super(Attivita, self).save(*args, **kwargs)
        else:
            raise ValueError("Wrong value in field 'reputazione'")

    def update_reputazione(self):
        """Aggiorna la reputazione dell'attività

        Calcola la media ponderata dei voti delle recensioni e aggiorna il DB.
        :return:
        """
        recensioni = self.recensione_set.all()
        votoxaff = 0.
        aff_tot = 0
        for r in recensioni:
            votoxaff += r.voto * r.autore.affidabilita
            aff_tot += r.autore.affidabilita

        self.reputazione = votoxaff / max(aff_tot, 1)
        self.save()

    def get_relative_tagcloud_url(self):
        """Genera e ritorna l'url relativo della tagcloud dell'attività

        :return: url relativo della tagcloud
        :rtype str
        """
        return os.path.join('attivita', 'tagcloud', str(self.id) + '.png')

    def get_absolute_tagcloud_url(self):
        """Genera e ritorna l'url assoluto della tagcloud dell'attività

        :return: url assoluto della tagcloud
        :rtype str
        """
        path = os.path.join(BASE_DIR, 'attivita', 'static', self.get_relative_tagcloud_url())
        return path

    def update_tagcloud(self):
        """Aggiorna tagcloud dell'attività"""
        create_tag_cloud(self)


def get_upload_path(instance, filename):
    """Genera e ritorna il path di un'immagine

    :param instance: oggetto contenente l'immagine
    :param filename: nome file contenente l'immagine
    :return: path immagine
    :rtype str
    """
    if instance.tagcloud:
        path = os.path.join(BASE_DIR, 'attivita', 'static', 'attivita', 'tagcloud',
                            str(instance.attivita.id)+'.png')
    else:
        num_images = Image.objects.filter(attivita__id=instance.attivita.id).count()
        ext = instance.immagine.path.split('.')[-1]
        path = os.path.join(BASE_DIR, 'attivita', 'static', 'attivita',
                            str(instance.attivita.id), '{}.{}'.format(num_images+1, ext))
    print(path)
    return path


class Image(models.Model):
    """Definisce un'immagine

    Attributi:
        attivita (ForeignKey): chiave esterna all'attività dell'immagine
        titolo (CharField)
        immagine (ImageField)
        tagcloud (BooleanField): booleano che indica se l'immagine sia una tagcloud
    """
    attivita = models.ForeignKey(Attivita, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=20)
    immagine = models.ImageField(upload_to=get_upload_path)
    filename = models.CharField(max_length=250, default=None)
    tagcloud = models.BooleanField(default=False)

    def get_relative_path(self):
        """Ritorna url relativo immagine

        :return: url relativo immagine
        :rtype str
        """
        return os.path.join('attivita', str(self.attivita.id), self.filename)
