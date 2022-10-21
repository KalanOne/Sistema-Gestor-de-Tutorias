from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
import datetime
# Create your views here.

#Vistas para login, logout y pagina principal para todos los usuarios
def group_required(*group_names):
    """ Grupos, checar si pertenece a grupo """

    def check(user):
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    # Si no se pertenece al grupo, redirigir a /prohibido/
    return user_passes_test(check, login_url='inicioSesion')

def inicioSesion(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("User is logged in :)")
            print(f"Username --> {request.user.username}")
            print('grupos:', request.user.groups.all())
            return redirect('paginaInicio')
        else:
            print("User is not logged in :(")
            return render(request, 'login.html', {
                'title': 'SGT Login',
                'form': AuthenticationForm
            })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'title': 'SGT Login',
                'form': AuthenticationForm,
                'error': 'Usuario no encontrado'
            })
        else:
            login(request, user)
            return redirect('paginaInicio')

@login_required
def paginaInicio(request):
    return render(request, 'paginaInicio.html', {
        'gruops': request.user.groups.all(),
        'title': 'Página de inicio'
    })

@login_required
def cierreSesion(request):
    logout(request)
    return redirect('inicioSesion')




#Vistas para el perfil de tutorados
@login_required
@group_required('Tutorado')
def cuestionariosTutorado(request):
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    fecha = datetime.datetime.now()
    print(tutorado.idGrupo.id)
    return render(request, 'cuestionariosTutorado.html', {
        'gruops': request.user.groups.all(),
        'title': 'Cuestionarios',
        'cuestionarios': Cuestionario.objects.filter(idGrupo = tutorado.idGrupo.id, fechaLimite__gte = fecha.strftime("%Y-%m-%d"), idEstado = 1)
    })

@login_required
@group_required('Tutorado')
def perfilTutorado(request):
    #obtener objetos
    usuario=get_object_or_404(User, id=request.user.id)
    tutorado=get_object_or_404(Tutorado, user_id=request.user.id)
    departamentoacademico=get_object_or_404(DepartamentoAcademico, id=tutorado.idDepartamentoAcademico_id)

    try:
        padremadretutor=PadreMadreTutor.objects.get(id=tutorado.idPadreMadreTutor_id)
        padremadretutorform=PadreMadreTutorForm(instance=padremadretutor) 
    except:
        padremadretutorform=PadreMadreTutorForm() 
    
    try:
        grupo=Grupo.objects.get(id=tutorado.idGrupo_id)
        grupoform=GrupoForm(instance=grupo)
    except:
        grupoform=GrupoForm()

    #autorellenar forms con el instance
    usuarioform=UserForm(instance=usuario)
    perfilTutoradoform=PerfilTutoradoForm(instance=tutorado)
    departamentoacademicoform=DepartamentoAcademicoForm(instance=departamentoacademico)
    return render(request, 'perfilTutorado.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'formusuario': usuarioform,
        'formPerfilTutorado': perfilTutoradoform,
        'formpadremadretutor': padremadretutorform,
        'formgrupo': grupoform,
        'formdepartamentoacademico': departamentoacademicoform
    })


@login_required
@group_required('Tutorado')
def miscitas(request):
    return render(request, 'miscitas.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ayuda Psicologica'
    })

def a12(request):
    return render(request, 'Realizar cuestionario Tutorado.html')

@login_required
@group_required('Tutorado')
def cambiarPassword(request):
    return render(request, 'PerfilTutoradoContra.html',{
        'gruops': request.user.groups.all(),
        'title': 'Cambiar Contraseña'
    })

def a10(request):
    return render(request, 'Principal Tutorado.html')

def a5(request):
    return render(request, 'Credito complementario Tutorado Vista General.html')




#vistas para todos los perfiles menos el de tutorado
@login_required
@group_required('Tutor')
def Documentacion(request):
    return render(request, 'Documentacion.html',{
        'gruops': request.user.groups.all(),
        'title': 'Documentacion'
    })

@login_required
def verDocumentacion(request):
    return render(request, 'verDocumentacion.html')

@login_required
def crearDocumento(request):
    return render(request, 'crearDocumento.html')

@login_required
def perfilTodos(request):
    #obtener objetos
    usuario=get_object_or_404(User, id=request.user.id)
    personaltec=get_object_or_404(PersonalTec, user_id=request.user.id)
    departamentoacademico=get_object_or_404(DepartamentoAcademico, id=personaltec.idDepartamentoAcademico_id)

    #autorellenar forms con el instance
    usuarioform=UserForm(instance=usuario)
    perfilPersonalTecform=PerfilPersonalTecForm(instance=personaltec)
    departamentoacademicoform=DepartamentoAcademicoForm(instance=departamentoacademico)
    return render(request, 'perfilTodos.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'formusuario': usuarioform,
        'formperfilPersonalTec': perfilPersonalTecform,
        'formdepartamentoacademico': departamentoacademicoform
    })

def a2(request):
    return render(request, 'Creacion_usuarios_tutores.html')

@login_required
@group_required('Tutor')
def crearCuestionario(request):
    return render(request, 'crear_cuestionario.html',{
        'gruops': request.user.groups.all(),
        'title': 'Grupos'
    })

@login_required
@group_required('Tutor')
def gruposTutor(request):
    return render(request, 'Listado_Grupos_Tutor.html',{
        'gruops': request.user.groups.all(),
        'title': 'Grupos'
    })

def a11(request):
    return render(request, 'psicologo dar citas.html')

def a13(request):
    return render(request, 'reporte_semestral_tutor.html')

@login_required
@group_required('Tutor')
def cambiarPasswordTutor(request):
    return render(request, 'PerfilTutoradoContra.html',{
        'gruops': request.user.groups.all(),
        'title': 'Cambiar Contraseña'
    })




#pruebas
@login_required
def prueba(request):
    return render(request, 'prueba.html', {
        'groups': request.user.groups.all()
    })
