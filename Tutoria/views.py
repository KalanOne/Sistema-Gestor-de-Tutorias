from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cuestionario, Tutorado, Grupo
from django.utils.timezone import now
import datetime

# Create your views here.

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
@group_required('Tutor')
def Documentacion(request):
    return render(request, 'Documentacion.html')


@login_required
def prueba(request):
    return render(request, 'prueba.html', {
        'groups': request.user.groups.all()
    })


@login_required
def verDocumentacion(request):
    return render(request, 'verDocumentacion.html')


@login_required
def crearDocumento(request):
    return render(request, 'crearDocumento.html')


@login_required
def perfilTodos(request):
    return render(request, 'perfilTodos.html')


def a2(request):
    return render(request, 'Creacion_usuarios_tutores.html')


def a3(request):
    return render(request, 'creacionCuestionarios.html')


def a4(request):
    return render(request, 'crear_cuestionario.html')


def a5(request):
    return render(request, 'Credito complementario Tutorado Vista General.html')


def a6(request):
    return render(request, 'Listado_Grupos_Tutor.html')

@login_required
@group_required('Tutorado')
def miscitas(request):
    return render(request, 'miscitas.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ayuda Psicologica'
    })


def a8(request):
    return render(request, 'Perfil Tutorado Contra.html')

@login_required
@group_required('Tutorado')
def perfilTutorado(request):
    return render(request, 'perfilTutorado.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil'
    })


def a10(request):
    return render(request, 'Principal Tutorado.html')


def a11(request):
    return render(request, 'psicologo dar citas.html')


def a12(request):
    return render(request, 'Realizar cuestionario Tutorado.html')


def a13(request):
    return render(request, 'reporte_semestral_tutor.html')


