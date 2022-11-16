from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from tablib import Dataset 
from django.utils.datastructures import MultiValueDictKeyError

from Tutoria.resources import ExcelResource
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
    padremadretutor=get_object_or_404(PadreMadreTutor, id=tutorado.idPadreMadreTutor_id)
    grupo=get_object_or_404(Grupo, id=tutorado.idGrupo_id)
    departamentoacademico=get_object_or_404(DepartamentoAcademico, id=tutorado.idDepartamentoAcademico_id)

    #autorellenar forms con el instance
    usuarioform=UserForm(instance=usuario)
    perfilTutoradoform=PerfilTutoradoForm(instance=tutorado)
    padremadretutorform=PadreMadreTutorForm(instance=padremadretutor) 
    grupoform=GrupoForm(instance=grupo)
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




#pruebas
@login_required
def prueba(request):
    return render(request, 'prueba.html', {
        'groups': request.user.groups.all()
    })

#vista subir credito
@login_required
@group_required('Tutorado')
def subir_credito(request):
    tutorado=Tutorado.objects.get(user_id = request.user.id)
    if request.method == 'POST':  
        print(tutorado) 
        fileTitle = request.POST['nombre']
        print(fileTitle)
    try:        
        
        uploadedFile = request.FILES['constancia_credito']

    except MultiValueDictKeyError:
        return render(request, 'subir_credito.html',{
            'gruops': request.user.groups.all(),
            'title': 'Creditos complementarios'
        })
    from Tutoria.models import Credito
    cdt=Credito.objects.create(nombre_doc = fileTitle, archivo = uploadedFile, idEstado = 0, idTutorado = tutorado)  
    print(fileTitle)   
    print(uploadedFile) 
    print(tutorado) 
    return render(request, 'subir_credito.html',{
        'gruops': request.user.groups.all(),
        'title': 'Creditos complementarios'
    })
       
#vista editar credito
@login_required
@group_required('Tutorado')
def editar_credito(request, dato):
    if request.method == 'POST':  
        #como recibir los datos?
        fileTitle = request.POST['nombre']
        try:        
        
            uploadedFile = request.FILES['constancia_credito']

        except MultiValueDictKeyError:
            return render(request, 'editar_credito.html',{
                'gruops': request.user.groups.all(),
                'title': 'Creditos complementarios'
            })

        print(dato)
        from Tutoria.models import Credito
        cdt=Credito.objects.filter(id = dato).update(nombre_doc = fileTitle, archivo = uploadedFile, idEstado = 0)
        return render(request, 'editar_credito.html',{
            'title': 'Creditos complementarios'
        })
    
    return render(request, 'editar_credito.html',{
        'title': 'Creditos complementarios'
    })

#vista revisar credito
@login_required
@group_required('Encargado Creditos')
def revisar_credito(request, dato):
    
    if request.method == 'POST':  
        #como recibir los datos?
        advise = request.POST['comentarios']
        print(advise)
        choice = request.POST['desicion']
        print(choice)
        print(dato)
        from Tutoria.models import Credito
        cdt=Credito.objects.filter(id = dato).update(comentarios=advise, idEstado=choice)
        return render(request, 'revisar_credito.html',{
            'title': 'Creditos complementarios'
        })
    
    return render(request, 'revisar_credito.html',{
        'title': 'Creditos complementarios'
    })

#Vista ver creditos tutorado
@login_required
@group_required('Tutorado')
def ver_credito_tutorado(request):
    if request.method == 'POST':  
        
        dato = request.POST['Id']
        print(dato)
        return redirect('editar_credito', dato)
    
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    print(tutorado)
    return render(request, 'ver_credito_tutorado.html', {
        'title': 'Ver creditos',
        'Credito': Credito.objects.filter(idTutorado = tutorado)
    })

#Vista ver creditos encargado
@login_required
@group_required('Encargado Creditos')
def ver_credito_tutor(request):

    if request.method == 'POST':  
        
        dato = request.POST['Id']
        print(dato)
        return redirect('revisar_credito', dato)
    encargado = PersonalTec.objects.get(user_id = request.user.id)
    carrera = encargado.idDepartamentoAcademico
    print(carrera)
    alumnos = Tutorado.objects.filter(idDepartamentoAcademico = carrera).values('id')
    print(alumnos)

    return render(request, 'ver_credito_tutor.html', {
        'title': 'Revisar creditos',
        
        'Credito': Credito.objects.filter(idTutorado__in = alumnos, idEstado = 0)
        
    })

#Vista subir datos excel 
from tablib import Dataset 

def Excel2(request):  
    if request.method == 'POST':  
        persona_resource = ExcelResource()  
        dataset = Dataset()  
     #print(dataset)  para la comprobacion
    try:
        nuevas_personas = request.FILES['excel_file']  
    except MultiValueDictKeyError:
        return render(request, 'excel2.html')
     #print(nuevas_personas)  para ver si se guardaron los datos
    imported_data = dataset.load(nuevas_personas.read())  
     #print(dataset)  
    result = persona_resource.import_data(dataset, dry_run=True) # Test the data import  
    print(result.has_errors())  
    if not result.has_errors():  
        persona_resource.import_data(dataset, dry_run=False) # Actually import now  
        from Tutoria.models import Excel2
        from Tutoria.models import Tutorado
        from django.contrib.auth.models import User
        for Alumno in Excel2.objects.all():
            #print(Alumno.control)
            usr=User.objects.create(username=Alumno.control, password=Alumno.email)
        
        limpiar = Excel2.objects.all()
        limpiar.delete()
        return render(request, 'excel2.html')  
