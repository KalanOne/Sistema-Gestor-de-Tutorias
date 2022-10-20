from django import forms
from django.forms import Widget
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
        }

class PerfilTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = '__all__'
        widgets = {
            'domicilio': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'correoPersonal': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'semestre': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'})
        }


class PadreMadreTutorForm(forms.ModelForm):
    class Meta:
        model = PadreMadreTutor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'apellidoPaterno': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'apellidoMaterno': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'})
        }