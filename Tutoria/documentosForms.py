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
            'credito': ('(Si/No)'),
            'estudianteCanalizado': ('')
        }
        widgets = {
            'estudianteCanalizado': forms.NumberInput(attrs={'min' : 0}),
            'asistencia': forms.NumberInput(attrs={'min' : 0, 'max' : 100})
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

class CambioPeriodo(forms.ModelForm):
    class Meta:
        model = FechaLimite
        exclude = {'ano', 'periodo', 'institucion'}
        labels = {
            'diagnosticoInstitucional': ('Fecha límite para Diagnóstico Institucional'),
            'planAccionTutorial': ('Fecha límite para Plan de Acción Tutorial Departamental'),
            'programaInstitucionalTutorial': ('Fecha límite para Programa Institucional Tutorial'),
            'reporteSemestralGrupal': ('Fecha límite para Reporte Semestral Grupal'),
            'reporteSemestralDepartamental': ('Fecha límite para Reporte Semestral Departamental'),
            'reporteSemestralInstitucional': ('Fecha límite para Reporte Semestral Departamental')
        }
        widgets = {
            'diagnosticoInstitucional': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'planAccionTutorial': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'programaInstitucionalTutorial': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'reporteSemestralGrupal': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'reporteSemestralDepartamental': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'reporteSemestralInstitucional': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaDiagnostico(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'diagnosticoInstitucional'}
        labels = {
            'diagnosticoInstitucional': ('Nueva fecha límite para Diagnóstico Institucional'),
        }
        widgets = {
            'diagnosticoInstitucional': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaPAT(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'planAccionTutorial'}
        labels = {
            'planAccionTutorial': ('Nueva fecha límite para Plan de Acción Tutorial Departamental'),
        }
        widgets = {
            'planAccionTutorial': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaPIT(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'programaInstitucionalTutorial'}
        labels = {
            'programaInstitucionalTutorial': ('Nueva fecha límite para Programa Institucional Tutorial'),
        }
        widgets = {
            'programaInstitucionalTutorial': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaReporteGrupal(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'reporteSemestralGrupal'}
        labels = {
            'reporteSemestralGrupal': ('Nueva fecha límite para Reporte Semestral Grupal'),
        }
        widgets = {
            'reporteSemestralGrupal': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaReporteDepartamental(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'reporteSemestralDepartamental'}
        labels = {
            'reporteSemestralDepartamental': ('Nueva fecha límite para Reporte Semestral Departamental'),
        }
        widgets = {
            'reporteSemestralDepartamental': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }

class ModFechaReporteInstitucional(forms.ModelForm):
    class Meta:
        model = FechaLimite
        fields = {'reporteSemestralInstitucional'}
        labels = {
            'reporteSemestralInstitucional': ('Nueva fecha límite para Reporte Semestral Institucional'),
        }
        widgets = {
            'reporteSemestralInstitucional': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()})
        }