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

class RegistrarUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username','first_name','last_name','email'}
        labels = {
            'username': ('Nombre de usuario'),
            'first_name': ('Nombre'),
            'last_name': ('Apellidos'),
            'email': ('Correo Institucional')
        }
        widgets = {
            'username': forms.TextInput(attrs={'required':'true'}),
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
            'email': forms.EmailInput(attrs={'required':'true'}),
        }

class EditarUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_first_name','required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'id':'User_last_name','required':'true'}),
        }

class EditarUserTutoradoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
        }
        labels = {
            'first_name': ('Nombre'),
            'last_name': ('Apellidos'),
        }

class EditarUserPersonalTecForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
        }
        labels = {
            'first_name': ('Nombre'),
            'last_name': ('Apellidos'),
        }

class MostrarUserTutoradoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username','first_name','last_name','email'}
        widgets = {
            'username': forms.TextInput(attrs={'required':'true'}),
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
            'email': forms.EmailInput(attrs={'required':'true'}),
        }
        labels = {
            'username': ('Numero de Control'),
            'first_name': ('Nombre'),
            'last_name': ('Apellidos'),
            'email': ('Correo Institucional')
        }

class MostrarUserTodosForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name','last_name','email'}
        widgets = {
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'last_name': forms.TextInput(attrs={'required':'true'}),
            'email': forms.EmailInput(attrs={'required':'true'}),
        }
        labels = {
            'first_name': ('Nombre'),
            'last_name': ('Apellidos'),
            'email': ('Correo Institucional')
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

class MostrarPerfilTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = {'domicilio','telefono','correoPersonal','semestre'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'required':'true'}),
            'telefono': forms.TextInput(attrs={'required':'true'}),
            'correoPersonal': forms.TextInput(attrs={'required':'true'}),
            'semestre': forms.EmailInput(attrs={'required':'true'}),
        }

class EditarPerfilTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = {'domicilio','telefono','correoPersonal'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'required':'true'}),
            'telefono': forms.TextInput(attrs={'required':'true'}),
            'correoPersonal': forms.TextInput(attrs={'required':'true'})
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

class MostrarGrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = {'grupo'}
        widgets = {
            'grupo': forms.TextInput()
        }

class DepartamentoAcademicoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoAcademico
        fields = '__all__'
        widgets = {
            'departamentoAcademico': forms.TextInput(attrs={'class':'form-control', 'id':'DepartamentoAcademico_departamentoAcademico'}),
            'abreviacion': forms.TextInput(attrs={'class':'form-control', 'id':'DepartamentoAcademico_abreviacion'})
        }

class MostrarPadreMadreForm(forms.ModelForm):
    class Meta:
        model = PadreMadreTutor
        fields = {'nombre','apellidos','telefonotutor'}
        labels = {
            'telefonotutor': ('Telefono del Tutor')
        }

class EditarPadreMadreForm(forms.ModelForm):
    class Meta:
        model = PadreMadreTutor
        fields = {'nombre','apellidos','telefonotutor'}

class MostrarDepartamentoAcademicoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoAcademico
        fields = {'departamentoAcademico'}
        labels = {
            'departamentoAcademico': ('Departamento Académico')
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

class MostrarPerfilPersonalTecForm(forms.ModelForm):
    class Meta:
        model = PersonalTec
        fields = {'domicilio','telefono', 'correoPersonal','edificio'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'required':'true'}),
            'telefono': forms.TextInput(attrs={'required':'true'}),
            'correoPersonal': forms.TextInput(attrs={'required':'true'}),
            'edificio': forms.TextInput(attrs={'required':'true'})
        }

class EditarPerfilPersonalTecForm(forms.ModelForm):
    class Meta:
        model = PersonalTec
        fields = {'domicilio','telefono', 'correoPersonal','edificio'}
        widgets = {
            'domicilio': forms.TextInput(attrs={'required':'true'}),
            'telefono': forms.TextInput(attrs={'required':'true'}),
            'correoPersonal': forms.TextInput(attrs={'required':'true'}),
            'edificio': forms.TextInput(attrs={'required':'true'})
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
        model = registrarAlumno
        fields = {'archivo'}

class RegistrarPersonalTecForm(forms.ModelForm):
    archivo= forms.FileField()
    class Meta:
        model = registrarPersonalTec
        fields = {'archivo'}

class RegistrarPersonalTecForm2(forms.ModelForm):
    class Meta:
        model = PersonalTec
        fields = {'idDepartamentoAcademico'}
        labels = {
            'idDepartamentoAcademico': ('Departamento Académico')
        }
        widgets = {
            'idDepartamentoAcademico': forms.Select(attrs={'required':'true'})
        }

class SubirCreditoForm(forms.ModelForm):
    class Meta:
        model = Credito
        fields = {'nombre_doc','archivo'}
        labels = {
            'archivo': ('Sube tu archivo')
        }

class DecisionCreditoForm(forms.ModelForm):
    class Meta:
        model = Credito
        fields = {'idEstado','comentarios'}
        labels = {
            'idEstado': ('Seleccione el estado del credito'),
            'comentarios': ('Comentarios')
        }

class SolicitudCitaPsicologo(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'idMotivo', 'descripcion', 'fechaCita', 'horaCanalizacion', 'lugar', 'idTutorado'}
        labels = {
            'idMotivo': ('Motivo'),
            'descripcion': ('Descripción'),
            'fechaCita': ('Fecha'),
            'horaCanalizacion': ('Hora'),
            'lugar': ('Lugar'),
            'idTutorado': ('Tutorado'),
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows' : 3}),
            'fechaCita': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today(),}),
            'horaCanalizacion': forms.TimeInput(attrs={'type': 'time'}),
        }
        required = {'descripcion', 'fechaCita', 'horaCanalizacion', 'lugar'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

class AsignarCitaPricologo(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'fechaCita', 'horaInicio', 'horaFinal', 'lugar'}
        labels = {
            'fechaCita': ('Fecha'),
            'horaInicio': ('Rango de hora (Inicio)'),
            'horaFinal': ('Rango de hora (Final)'),
            'lugar': ('Lugar'),
        }
        widgets = {
            'fechaCita': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'horaCanalizacion': forms.TimeInput(attrs={'type': 'time'}),
            'horaInicio': forms.TimeInput(attrs={'type': 'time'}),
            'horaFinal': forms.TimeInput(attrs={'type': 'time'})
        }
        required = {'fechaCita', 'horaInicio', 'lugar', 'horaFinal'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

class ConcluirCitaPsicologo(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'horaCanalizacion', 'idEstado'}
        labels = {
            'horaCanalizacion': ("Hora canalizada"),
            'idEstado': ('Estado final'),
        }
        widgets = {
            'horaCanalizacion': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estadoAceptado = Estado.objects.get(estado = 'Atendido')
        estadoRechazado = Estado.objects.get(estado = 'No atendido')
        elecciones = [
            ("", "------"),
            (estadoAceptado.id, estadoAceptado.estado),
            (estadoRechazado.id, estadoRechazado.estado)
        ]
        self.fields['idEstado'].choices = elecciones

class RegistroCitaMedico(forms.ModelForm):
    class Meta:
        model = Cita
        fields = {'fechaCita', 'horaCanalizacion', 'lugar', 'descripcion', 'idMotivo', 'idTutorado'}
        labels = {
            'fechaCita': ('Fecha de atención'),
            'horaCanalizacion': ('Hora de atención'),
            'lugar': ('Lugar de atención'),
            'descripcion': ('Descripción'),
            'idMotivo': ('Motivo de atención'),
            'idTutorado': ('Tutorado')
        }
        widgets = {
            'fechaCita': forms.DateInput(attrs={'type': 'date'}),
            'horaCanalizacion': forms.TimeInput(attrs={'type': 'time'}),
            'descripcion': forms.Textarea(attrs={'rows' : 5}),
        }
        required = {'fechaCita', 'horaCanalizacion', 'lugar', 'descripcion', 'idMotivo', 'idTutorado'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True
        ordenMedi = Orden.objects.get(nombreOrden = 'Médico')
        motivos = Motivo.objects.filter(idOrden_id = ordenMedi.id)
        self.fields['idMotivo'].choices = [(motivo.id, motivo.nombre) for motivo in motivos]

class CrearDepartamentoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoAcademico
        fields = {'departamentoAcademico','abreviacion'}
        labels = {
            'departamentoAcademico': ('Nombre del Departamento')
        }