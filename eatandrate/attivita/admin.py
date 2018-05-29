"""Determina il contenuto legato alle attività della sezione Admin

Aggiunge la lista delle attività, mostrando il nome e la relativa reputazione
nell'indice e aggiunge un campo di ricerca per nome delle attività.
Ogni attività contiene nella pagina dedicata anche le relative recensioni
e immagini
"""

from django.contrib import admin
from .models import Attivita, Image, Tipologia
from recensioni.models import Recensione


class RecensioneInline(admin.StackedInline):
    """Aggiunge le recensioni di un'attività alla relativa pagina nella sezione admin"""
    model = Recensione
    extra = 0
    classes = ['collapse']


class ImageInline(admin.StackedInline):
    """Aggiunge le recensioni di un'attività alla relativa pagina nella sezione admin"""
    model = Image
    extra = 0
    classes = ['collapse']


class AttivitaAdmin(admin.ModelAdmin):
    """Definisce i contenuti delle pagine Admin relative alle attività

    Nell'indice delle attività viene mostrato il nome e la reputazione per ciascuna di esse
    e viene aggiunto un campo di ricerca.
    Nella pagina di ogni singola attività vengono aggiunte relative recensioni e immagini.
    """
    inlines = [RecensioneInline, ImageInline]
    list_display = ('nome', 'reputazione',)
    list_filter = ['nome', 'tipologie']
    search_fields = ['nome']


admin.site.register(Attivita, AttivitaAdmin)
admin.site.register(Tipologia)
