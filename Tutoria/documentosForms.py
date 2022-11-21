from django import forms
from django.forms import Widget
from .models import *
from django.contrib.auth.models import User
import datetime
from .documentosModels import *

class FormTutoradoReporteSemestralGrupalCreditoV2(forms.ModelForm):
    class Meta:
        model = TutoradoReporteSemestralGrupalV2
        exclude = {'reporte'}
        labels = {
            'tutorado': (''),
            'tutoriaGrupal': (''),
            'tutoriaIndividual': (''),
            'observaciones': (''),
            'asistencia': (''),
            'credito': (''),
            'estudianteCanalizado': ('')
        }
        widgets = {
            'estudianteCanalizado': forms.Textarea(attrs={'rows' : 2})
        }

class FormReporteSemestralDepartamentalV2(forms.ModelForm):
    class Meta:
        model = ReporteSemestralDepartamentalV2
        exclude = {'archivo', 'ano', 'periodo', 'fecha', 'departamento', 'coordinador', 'estado'}
        labels = {
            'actividad1': ('Actividad 1 más importante realizada en el semestre'),
            'actividad2': ('Actividad 2 más importante realizada en el semestre'),
            'actividad3': ('Actividad 3 más importante realizada en el semestre'),
            'actividad4': ('Actividad 4 más importante realizada en el semestre'),
            'actividad5': ('Actividad 5 más importante realizada en el semestre'),
            'actividad6': ('Actividad 6 más importante realizada en el semestre'),
            'actividad7': ('Actividad 7 más importante realizada en el semestre'),
            'actividad8': ('Actividad 8 más importante realizada en el semestre'),
            'actividad9': ('Actividad 9 más importante realizada en el semestre'),
            'actividad10': ('Actividad 10 más importante realizada en el semestre'),
            'acciones': ('Acciones de mayor impacto para alcanzar la competencia de la asignatura')
        }
        widgets = {
            'actividad1': forms.Textarea(attrs={'rows' : 5}),
            'actividad2': forms.Textarea(attrs={'rows' : 5}),
            'actividad3': forms.Textarea(attrs={'rows' : 5}),
            'actividad4': forms.Textarea(attrs={'rows' : 5}),
            'actividad5': forms.Textarea(attrs={'rows' : 5}),
            'actividad6': forms.Textarea(attrs={'rows' : 5}),
            'actividad7': forms.Textarea(attrs={'rows' : 5}),
            'actividad8': forms.Textarea(attrs={'rows' : 5}),
            'actividad9': forms.Textarea(attrs={'rows' : 5}),
            'actividad10': forms.Textarea(attrs={'rows' : 5}),
        }

class FormTutorReporteSemestralDepartamentalV2(forms.ModelForm):
    class Meta:
        model = TutorReporteSemestralDepartamentalV2
        exclude = {'reporte'}
        labels = {
            'tutoriaGrupal': '',
            'tutoriaIndividual': '',
            'estudianteCanalizado': '',
            'areaCanalizada': '',
            'tutor': '',
            'grupo': ''
        }
        widgets = {
            'estudianteCanalizado': forms.Textarea(attrs={'rows' : 2}),
            'areaCanalizada': forms.Textarea(attrs={'rows' : 2})
        }

class FormPATDepartamentalV2(forms.ModelForm):
    class Meta:
        model = PATDepartamentalV2
        fields = {'archivo'}
        labels = {
            'archivo': ('Selecciona tu archivo')
        }

class FormDiagnosticoInstitucionalV2(forms.ModelForm):
    class Meta:
        model = DiagnosticoInstitucionalV2
        fields = {'archivo'}
        labels = {
            'archivo': ('Selecciona tu archivo')
        }

class FormConfirmacionReporteInstitucional(forms.Form):
    confirmacion = forms.HiddenInput()