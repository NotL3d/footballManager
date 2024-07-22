from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from home.models import CustomUserModel, Player, SelectedPlayer, ChooseTeamModel
from django.forms.widgets import Select



# form create user
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_day', 'gender']
        widgets = {
            "birth_day": forms.DateInput(attrs={'class': 'form-control', 'type': "date"})

        }

    # edit label and help text for user registration form
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


# update form for user
class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ['first_name', 'last_name', 'gender', 'birth_day']
        exclude = ['username', 'email']
        widgets = {
            "birth_day": forms.DateInput(attrs={'class': 'form-control', 'type': "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Numele de familie'
        self.fields['last_name'].label = 'Nume'
        self.fields['birth_day'].label = 'Ziua de naștere'
        self.fields['gender'].label = 'Sexul'
        self.fields['birth_day'].help_text = "* Selectati data de naștere!"

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Numele de familie'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nume'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'form-control',
        })

        if 'password' in self.fields:
            self.fields['password'].help_text = ''
            self.fields['password'].widget = forms.HiddenInput()


# authentication form
class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Utilizator'
        self.fields['password'].label = 'Parola'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})



class CustomSelectWidget(Select):
    def __init__(self, attrs=None, choices=()):
        attrs = attrs or {}
        attrs.update({'class': 'form-select'})  # Add Bootstrap custom-select class
        super().__init__(attrs=attrs, choices=choices)

class PlayerSelectionForm(forms.Form):
    goalkeeper = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Select 1 goalkeeper',
        widget=CustomSelectWidget()
    )
    attacker_1 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează primul atacant',
        widget=CustomSelectWidget()
    )
    attacker_2 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 2-lea atacant',
        widget=CustomSelectWidget()
    )
    defender = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează primul apărător',
        widget=CustomSelectWidget()
    )
    defender_2 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 2-lea apărător',
        widget=CustomSelectWidget()
    )
    defender_3= forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 3- lea apărător',
        widget=CustomSelectWidget()
    )
    defender_4 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 4-lea apărător',
        widget=CustomSelectWidget()
    )
    midfielder = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează primul mijlocaș',
        widget=CustomSelectWidget()
    )
    midfielder_2 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 2-lea mijlocaș',
        widget=CustomSelectWidget()
    )
    midfielder_3 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 3-lea mijlocaș',
        widget=CustomSelectWidget()
    )
    midfielder_4 = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        label='Selectează al 4-lea mijlocaș',
        widget=CustomSelectWidget()
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            chosen_team = ChooseTeamModel.objects.get(user=user)
            self.fields['goalkeeper'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['attacker_1'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['attacker_2'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['defender'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['defender_2'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['defender_3'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['defender_4'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['midfielder'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['midfielder_2'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['midfielder_3'].queryset = Player.objects.filter(team=chosen_team.team)
            self.fields['midfielder_4'].queryset = Player.objects.filter(team=chosen_team.team)
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data












