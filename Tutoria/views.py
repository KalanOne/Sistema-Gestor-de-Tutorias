from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.
def inicioSesion(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("User is logged in :)")
            print(f"Username --> {request.user.username}")
            return render(request, 'Documentacion.html')
        else:
            print("User is not logged in :(")
            return render(request, 'login.html', {
                'title': 'SGT Login',
                'form': AuthenticationForm
            })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
            'title': 'SGT Login',
            'form': AuthenticationForm,
            'error': 'Usuario no encontrado'
            })
        else:
            login(request, user)
            return HttpResponse('<h1>Hola</h1>')

@login_required
def Documentacion(request):
    return render(request, 'Documentacion.html')

@login_required
def verDocumentacion(request):
    return render(request, 'verDocumentacion.html')

@login_required
def crearDocumento(request):
    return render(request, 'crearDocumento.html')

@login_required
def perfilTodos(request):
    return render(request, 'perfilTodos.html')

@login_required
def a1(request):
    return render(request, 'citaspsicologo.html')

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

def a7(request):
    return render(request, 'miscitas.html')

def a8(request):
    return render(request, 'Perfil Tutorado Contra.html')
    
def a9(request):
    return render(request, 'perfilTutorado.html')

def a10(request):
    return render(request, 'Principal Tutorado.html')

def a11(request):
    return render(request, 'psicologo dar citas.html')

def a12(request):
    return render(request, 'Realizar cuestionario Tutorado.html')

def a13(request):
    return render(request, 'reporte_semestral_tutor.html')