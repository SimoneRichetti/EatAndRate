from django import forms
from django.forms import ModelForm
from .models import RicercaComplessa


class RicercaComplessaForm(ModelForm):
    """Form create dal modello `RicercaComplessa`"""
    testo_nome = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    testo_citta = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))

    class Meta:
        model = RicercaComplessa
        fields = ['testo_nome', 'testo_citta']
