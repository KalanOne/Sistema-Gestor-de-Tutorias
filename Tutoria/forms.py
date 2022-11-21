from django import forms
from django.forms import Widget
from .models import *
from django.contrib.auth.models import User
import datetime
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'id':'User_username','required':'true'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_first_name','required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_last_name','required':'true'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'id':'User_email','required':'true'}),
        }

class EditarUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_first_name','required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_last_name','required':'true'}),
        }

class PerfilTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = '__all__'
        widgets = {
            'domicilio': forms.TextInput(attrs={'class':'form-control', 'id':'Tutorado_domicilio'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'id':'Tutorado_telefono'}),
            'correoPersonal': forms.TextInput(attrs={'class':'form-control', 'id':'Tutorado_correoPersonal'}),
            'semestre': forms.TextInput(attrs={'class':'form-control', 'id':'Tutorado_semestre'})
        }

class PadreMadreTutorForm(forms.ModelForm):
    class Meta:
        model = PadreMadreTutor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'id':'PadreMadreTutor_nombre'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control', 'id':'PadreMadreTutor_apellidos', 'hidden':'true'}),
            'telefonotutor': forms.TextInput(attrs={'class':'form-control', 'id':'PadreMadreTutor_telefono'})
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'grupo': forms.TextInput(attrs={'class':'form-control', 'id':'Grupo_grupo'})
        }

class DepartamentoAcademicoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoAcademico
        fields = '__all__'
        widgets = {
            'departamentoAcademico': forms.TextInput(attrs={'class':'form-control', 'id':'DepartamentoAcademico_departamentoAcademico'}),
            'abreviacion': forms.TextInput(attrs={'class':'form-control', 'id':'DepartamentoAcademico_abreviacion'})
        }

class PerfilPersonalTecForm(forms.ModelForm):
    class Meta:
        model = PersonalTec
        fields = '__all__'
        widgets = {
            'domicilio': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_domicilio'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_telefono'}),
            'correoPersonal': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_correoPersonal'}),
            'edificio': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_edificio'})
        }

class EditarPerfilPersonalTecForm(forms.ModelForm):
    class Meta:
        model = PersonalTec
        fields = {'domicilio','telefono', 'correoPersonal'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_domicilio'}),
            'telefono': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_telefono'}),
            'correoPersonal': forms.TextInput(attrs={'class':'form-control', 'id':'PersonalTec_correoPersonal'}),
        }

class EnviarCuestionario(forms.ModelForm):
    class Meta:
        model = CuestionarioContestado
        fields = {'archivo'}
        labels = {
            'archivo': ('Sube tu archivo')
        }
        widgets = {
            'archivo': forms.FileInput(attrs={'accept' : 'application/pdf'}),
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = {'grupo','idEstado'}
        labels = {
            'grupo': ('Grupo'),
            'idEstado': ('Estado')
        }
    

class SolicitudCitaFormTutorado(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'idMotivo', 'descripcion'}
        labels = {
            'idMotivo': ('Motivo'),
            'descripcion': ('Descripción (Opcional)')
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows' : 5})
        }

class SolicitudCitaFormTutor(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'idMotivo', 'descripcion'}
        labels = {
            'idMotivo': ('Motivo'),
            'descripcion': ('Descripción')
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows' : 5})
        }
        required = {'descripcion'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

class CrearCuestionarioForm(forms.ModelForm):
    class Meta:
        model = Cuestionario
        fields = {'nombre', 'fechaLimite', 'archivo', 'idGrupo'}
        labels = {
            'nombre': ('Nombre de cuestionario'),
            'fechaLimite': ('Fecha límite'),
            'archivo': ('Archivo'),
            'idGrupo': ('Grupo')
        }
        widgets = {
            'fechaLimite': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today(),})
        }

class CambioDePeriodoInstitucion(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = {'anoActual', 'periodoActual'}
        labels = {
            'anoActual': ('Año nuevo'),
            'periodoActual': ('Periodo nuevo')
        }

class SubirReporteSemestralGrupal(forms.ModelForm):
    class Meta:
        model = ReporteSemestralGrupal
        fields = {'archivo', 'idGrupo'}
        labels = {
            'archivo': ('Sube tu archivo'), 
            'idGrupo': ('Grupo')
        }

class SubirReporteSemestralDept(forms.ModelForm):
    class Meta:
        model = ReporteSemestralDepartamento
        fields = {'archivo'}
        labels = {
            'archivo': ('Sube tu archivo')
        }

class SubirPAT(forms.ModelForm):
    class Meta:
        model = PAT
        fields = {'archivo'}
        labels = {
            'archivo': ('Sube tu archivo')
        }

class SubirReporteSemestralInst(forms.ModelForm):
    class Meta:
        model = ReporteSemestralInstitucional
        fields = {'archivo'}
        labels = {
            'archivo': ('Sube tu archivo')
        }

class CambiarPasswordForm(PasswordChangeForm):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')


class RegistrarTutoradosForm(forms.ModelForm):
    archivo= forms.FileField()
    class Meta:
        model = Excel2
        fields = {'archivo'}