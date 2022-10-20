from django import forms
from django.forms import Widget
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name','email'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
        }

    nombrecompleto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}))

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        usando = kwargs.pop('usando')
        super(UserForm, self).__init__(*args, **kwargs)

        if(usando):
            self.fields['first_name'].widget.attrs={'class':'form-control', 'disabled':'true','value':usuario.first_name}
            self.fields['last_name'].widget.attrs={'class':'form-control', 'disabled':'true','value':usuario.last_name}
            self.fields['nombrecompleto'].widget.attrs={'class':'form-control', 'disabled':'true','value':usuario.first_name + ' ' + usuario.last_name}
            self.fields['email'].widget.attrs={'class':'form-control', 'disabled':'true','value':usuario.email}


class perfilTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = {'domicilio','telefono','correoPersonal','semestre'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'correoPersonal': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'semestre': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'})
        }

    def __init__(self, *args, **kwargs):
        tutorado = kwargs.pop('tutorado')
        usando = kwargs.pop('usando')
        super(perfilTutoradoForm, self).__init__(*args, **kwargs)

        if(usando):
            self.fields['domicilio'].widget.attrs={'class':'form-control', 'disabled':'true','value':tutorado.domicilio}
            self.fields['telefono'].widget.attrs={'class':'form-control', 'disabled':'true','value':tutorado.telefono}
            self.fields['correoPersonal'].widget.attrs={'class':'form-control', 'disabled':'true','value':tutorado.correoPersonal}
            self.fields['semestre'].widget.attrs={'class':'form-control', 'disabled':'true','value':tutorado.semestre}


class PadreMadreTutorForm(forms.ModelForm):
    class Meta:
        model = PadreMadreTutor
        fields = {'nombre','apellidoPaterno','apellidoMaterno','telefono'}
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'apellidoPaterno': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'apellidoMaterno': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'disabled':'true'})
        }

    nombrecompleto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'disabled':'true'}))

    def __init__(self, *args, **kwargs):
        padremadretutor = kwargs.pop('padremadretutor')
        usando = kwargs.pop('usando')
        super(PadreMadreTutorForm, self).__init__(*args, **kwargs)

        if(usando):
            self.fields['nombre'].widget.attrs={'class':'form-control', 'disabled':'true','value':padremadretutor.nombre}
            self.fields['apellidoPaterno'].widget.attrs={'class':'form-control', 'disabled':'true','value':padremadretutor.apellidoPaterno}
            self.fields['apellidoMaterno'].widget.attrs={'class':'form-control', 'disabled':'true','value':padremadretutor.apellidoMaterno}
            self.fields['telefono'].widget.attrs={'class':'form-control', 'disabled':'true','value':padremadretutor.telefono}
            self.fields['nombrecompleto'].widget.attrs={'class':'form-control', 'disabled':'true','value':padremadretutor.nombre + ' ' + padremadretutor.apellidoPaterno + ' ' + padremadretutor.apellidoMaterno}