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
            'monto': forms.NumberInput(attrs={'type': 'number'}),
        }



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