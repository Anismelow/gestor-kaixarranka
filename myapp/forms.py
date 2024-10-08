from django import forms
from .models import *

class HorasForm(forms.ModelForm):
    class Meta:
        model = Horas
        fields = ['fecha', 'hora_entrada', 'hora_salida']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time'}),
        }



class AdelantoForm(forms.ModelForm):
    class Meta:
        model = Adelanto
        fields = ['fecha_solicitud', 'monto']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
            'monto': forms.NumberInput(attrs={'type': 'number', 'min': '0'}),
            
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto < 0:
            raise forms.ValidationError('El monto no puede ser negativo.')
        return monto



class UsersForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        label='Nombre de usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label='Contraseña'
    )


    # forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
