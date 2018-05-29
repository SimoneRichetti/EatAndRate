from django.forms import ModelForm, Textarea
from .models import Answer


class AnswerForm(ModelForm):
    """Form creato dal modello `Answer`"""
    class Meta:
        model = Answer
        fields = ['risposta']

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['risposta'].widget = Textarea(attrs={
            'id': 'answerfield',
            'class': 'noresize',
            'style': 'width:45%;resize:none;height:182px',
            'cols': 30,
            'rows': 9,
        })
