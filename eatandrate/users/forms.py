from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    """Form per la registrazione di un utente creato dal model `User` di Django"""
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    email = forms.CharField(max_length=254, help_text="Obbligatorio. Inserisci un indirizzo valido.",
                            widget=forms.TextInput(attrs={'style': 'width:auto'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    password1 = forms.CharField(max_length=30, label="Password",
                                widget=forms.TextInput(attrs={'type': 'password', 'style': 'width:auto'}))
    password2 = forms.CharField(max_length=30, label="Conferma Password",
                                widget=forms.TextInput(attrs={'type': 'password', 'style': 'width:auto'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserModifyForm(forms.ModelForm):
    """Form per la modifica di un utente creato dal model `User` di Django"""
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'style': 'width:auto'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class MyAuthenticationForm(AuthenticationForm):
    """Form per il login dell'utente.

    Estende il form di default di Django per integrarlo con Bootstrap
    """
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'style': 'width:auto'}))
    password = forms.CharField(max_length=30, label="Password",
                               widget=forms.TextInput(attrs={'type': 'password', 'style': 'width:auto'}))
