from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Event

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'Почта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}),
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        label='Пароль'
    )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'sponsor', 'place', 'type', 'event_date']