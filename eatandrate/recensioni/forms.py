from django.forms import ModelForm, TextInput, Textarea
from django.forms.widgets import ChoiceWidget, Select

from recensioni.models import Recensione


class RecensioneForm(ModelForm):
    """Form creato dal model `Recensione`"""
    class Meta:
        model = Recensione
        fields = ['voto', 'testo']

    def __init__(self, *args, **kwargs):
        super(RecensioneForm, self).__init__(*args, **kwargs)
        self.fields['testo'].widget = Textarea(attrs={
            'class': 'noresize',
            'style': 'width:auto;resize:none;height:182px',
            'cols': 30,
            'rows': 9
        })
