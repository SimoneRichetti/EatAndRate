from django.forms import Form, ModelForm, fields, TextInput, Textarea, FileInput
from .models import Attivita, Image


class AttivitaForm(ModelForm):
    """Form creato dal modello `Attivita`"""
    class Meta:
        model = Attivita
        fields = ['nome', 'indirizzo', 'citta', 'descrizione']

    def __init__(self, *args, **kwargs):
        super(AttivitaForm, self).__init__(*args, **kwargs)
        self.fields['indirizzo'].widget = TextInput(attrs={
            'placeholder': 'Via e Numero Civico',
            'style': 'width:auto'
        })
        self.fields['nome'].widget = TextInput(attrs={
            'style': 'width:auto'
        })
        self.fields['citta'].widget = TextInput(attrs={
            'style': 'width:auto'
        })
        self.fields['descrizione'].widget = Textarea(attrs={
            'class': 'noresize',
            'style': 'width:auto;resize:none;height:182px',
            'cols': 30,
            'rows': 9
        })


class UploadImageForm(ModelForm):
    """Form creato dal modello `Image`"""
    class Meta:
        model = Image
        fields = ['titolo', 'immagine']

    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['titolo'].widget = TextInput(attrs={
            'style': 'width:auto'
        })
        self.fields['immagine'].widget = FileInput(attrs={
            'style': 'width:auto'
        })


class TipologieForm(Form):
    """Form utilizzato per selezionare a quali tipologie appartiene un'attività"""
    Sushi = fields.BooleanField(required=False)
    Pizzeria = fields.BooleanField(required=False)
    Vegano = fields.BooleanField(required=False)
    Internazionale = fields.BooleanField(required=False)
    Pesce = fields.BooleanField(required=False)
    FastFood = fields.BooleanField(required=False)
    Birreria = fields.BooleanField(required=False)
    Tradizionale = fields.BooleanField(required=False)
    Cinese = fields.BooleanField(required=False)
    Barbecue = fields.BooleanField(required=False)
    Bar = fields.BooleanField(required=False)
