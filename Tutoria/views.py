from django.shortcuts import render, redirect
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
    if request.method == 'GET':
        usuario=request.user
        tutorado=Tutorado.objects.filter(user_id=request.user.id)
        if(tutorado.exists()):
            tutorado=Tutorado.objects.get(user_id=request.user.id)
            padremadretutor=PadreMadreTutor.objects.filter(id=tutorado.id)
            if(padremadretutor.exists()):
                padremadretutor=PadreMadreTutor.objects.get(id=tutorado.id)
                usuarioform=UserForm(usuario=usuario,usando=True)
                perfiltutoradoform=perfilTutoradoForm(tutorado=tutorado,usando=True)
                padremadretutorform=PadreMadreTutorForm(padremadretutor=padremadretutor,usando=True)
                return render(request, 'perfilTutorado.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Perfil',
                    'formPerfilTutorado':perfiltutoradoform,
                    'formpadremadretutor':padremadretutorform,
                    'formusuario':usuarioform
                })
            else:
                usuarioform=UserForm(usuario=usuario,usando=True)
                perfiltutoradoform=perfilTutoradoForm(tutorado=tutorado,usando=True)
                padremadretutorform=PadreMadreTutorForm(padremadretutor=padremadretutor,usando=False)
                return render(request, 'perfilTutorado.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Perfil',
                    'formPerfilTutorado':perfiltutoradoform,
                    'formpadremadretutor':padremadretutorform,
                    'formusuario':usuarioform
                })
        else:
                usuarioform=UserForm(usuario=usuario,usando=True)
                perfiltutoradoform=perfilTutoradoForm(tutorado=tutorado,usando=False)
                padremadretutorform=PadreMadreTutorForm(padremadretutor=padremadretutor,usando=False)
                return render(request, 'perfilTutorado.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Perfil',
                    'formPerfilTutorado':perfiltutoradoform,
                    'formpadremadretutor':padremadretutorform,
                    'formusuario':usuarioform
                })
    else:       
        print("hola")

@login_required
@group_required('Tutorado')
def miscitas(request):
    return render(request, 'miscitas.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ayuda Psicologica'
    })

def a12(request):
    return render(request, 'Realizar cuestionario Tutorado.html')

def a8(request):
    return render(request, 'Perfil Tutorado Contra.html')

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
    return render(request, 'perfilTodos.html',{
        'gruops': request.user.groups.all(),
        'title': 'Grupos'
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




#pruebas
@login_required
def prueba(request):
    return render(request, 'prueba.html', {
        'groups': request.user.groups.all()
    })
