from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from home.models import CustomUserModel


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_day', 'gender']
        widgets = {
            "birth_day": forms.DateInput(attrs={'class': 'form-control', 'type': "date"})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Utilizator'
        self.fields['first_name'].label = 'Numele de familie'
        self.fields['last_name'].label = 'Nume'
        self.fields['email'].label = 'Adresa de email'
        self.fields['birth_day'].label = 'Ziua de naștere'
        self.fields['gender'].label = 'Gen'
        self.fields['password1'].label = 'Parola'
        self.fields['password2'].label = 'Reintroduceti parola'
        self.fields['username'].help_text = "* Obligatoriu."
        self.fields['birth_day'].help_text = "* Selectati data de naștere!"
        self.fields['password1'].help_text = " * Parola nu trebuie sa fie similara cu alte informații personale!"
        self.fields['password1'].help_text += "<br> * Parola trebuie să conțină cel puțin 8 caractere!"
        self.fields['password1'].help_text += "<br> * Parola nu trebuie să fie o parolă asociată cu alte conturi!"
        self.fields['password1'].help_text += "<br> * Parola nu poate fi constituită doar din numere!"
        self.fields['password2'].help_text = "* Parola trebuie să fie asemănătoare cu prima introdusă!"
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Gândește-te la un username și scrie-l'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Scrie-ți numele de familie'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Scrie-ți prenumele tău'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Scrie o adresă de e-mail validă'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Scrie parola!'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Rescrie parola!'})


# authentication form

class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Utilizator'
        self.fields['password'].label = 'Parola'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})
