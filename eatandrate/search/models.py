from django.db import models
from attivita.models import Tipologia


# Create your models here.
class RicercaSemplice(models.Model):
    """Definisce una ricerca semplice

    Per ricerca semplice intendiamo un semplice ricerca TextField, senza filtro
    sulle tipologie delle attività

    Attibuti:
        testo (CharField)
    """
    testo = models.CharField(max_length=25)


class RicercaComplessa(models.Model):
    """Definisce una ricerca complessa

    Una ricerca è composta da una ricerca testuale per nome, una per città e
    un filtro sulle tipologie a cui l'attività deve appartenere

    Attibuti:
        testo_citta (CharField)
        testo_nome (CharField)
        tipologie (ManyToManyField)
    """
    testo_citta = models.CharField('citta', max_length=25, blank=True)
    testo_nome = models.CharField('nome', max_length=25, blank=True)
    tipologie = models.ManyToManyField(Tipologia, blank=True)
