from distutils.log import error
from this import d
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
import datetime
from django.contrib.auth.models import User
# Create your views here.

#Vistas para login, logout y pagina principal para todos los usuarios
def group_required(*group_names):
    """ Grupos, checar si pertenece a grupo """

    def check(user):
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    # Si no se pertenece al grupo, redirigir a pagina principal
    return user_passes_test(check, login_url='inicioSesion')

def guardarArchivo(file, ruta):
    try:
        with open(ruta, 'xb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True
    except:
        print('Aqui me paro 33')
        return False

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
    if request.user.groups.filter(name__in=['Tutorado']).exists():
        tutorado = Tutorado.objects.get(user_id = request.user.id)
        if tutorado.idGrupo is None:
            return render(request, 'paginaInicio.html', {
                'gruops': request.user.groups.all(),
                'title': 'Página de inicio',
                'cuentaGrupo': 0
            })
        else:
            return render(request, 'paginaInicio.html', {
                'gruops': request.user.groups.all(),
                'title': 'Página de inicio',
                'cuentaGrupo': 1
            })
    else:
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
    if tutorado.idGrupo is None:
        return redirect('paginaInicio')
    fecha = datetime.datetime.now()
    cuestionarios = Cuestionario.objects.filter(idGrupo = tutorado.idGrupo.id, fechaLimite__gte = fecha.strftime("%Y-%m-%d"))
    for cuestionario in cuestionarios.iterator():
        try:
            respondido = CuestionarioContestado.objects.get(idCuestionario_id = cuestionario.id, idTutorado_id = tutorado.id)
            cuestionarios.delete(cuestionario)
        except:
            print("Pasa")
    print(tutorado.idGrupo.id)
    return render(request, 'cuestionariosTutorado.html', {
        'gruops': request.user.groups.all(),
        'title': 'Cuestionarios',
        'cuentaGrupo': 1,
        'cuestionarios': cuestionarios
    })

@login_required
@group_required('Tutorado')
def perfilTutorado(request):
    #obtener objetos
    usuario = User.objects.get(id = request.user.id)
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    departamentoacademico = DepartamentoAcademico.objects.get(id = tutorado.idDepartamentoAcademico_id)
    
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1

    try:
        padremadretutor = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)
        padremadretutorform = PadreMadreTutorForm(instance = padremadretutor) 
        for fieldname in padremadretutorform.fields:
            padremadretutorform.fields[fieldname].disabled = True
    except:
        padremadretutorform = PadreMadreTutorForm() 
        for fieldname in padremadretutorform.fields:
            padremadretutorform.fields[fieldname].disabled = True
    
    try:
        grupo = Grupo.objects.get(id = tutorado.idGrupo_id)
        grupoform = GrupoForm(instance = grupo)
        for fieldname in grupoform.fields:
            grupoform.fields[fieldname].disabled = True
    except:
        grupoform = GrupoForm()
        for fieldname in grupoform.fields:
            grupoform.fields[fieldname].disabled = True

    #autorellenar forms con el instance
    usuarioform = UserForm(instance = usuario)
    for fieldname in usuarioform.fields:
        usuarioform.fields[fieldname].disabled = True

    perfilTutoradoform = PerfilTutoradoForm(instance = tutorado)
    for fieldname in perfilTutoradoform.fields:
        perfilTutoradoform.fields[fieldname].disabled = True

    departamentoacademicoform = DepartamentoAcademicoForm(instance = departamentoacademico)
    for fieldname in departamentoacademicoform.fields:
        departamentoacademicoform.fields[fieldname].disabled = True
        
    return render(request, 'perfilTutorado.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'cuentaGrupo': cuentaGrupo,
        'formusuario': usuarioform,
        'formPerfilTutorado': perfilTutoradoform,
        'formpadremadretutor': padremadretutorform,
        'formgrupo': grupoform,
        'formdepartamentoacademico': departamentoacademicoform
    })


@login_required
@group_required('Tutorado')
def editarInformacion(request):

    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1

    if request.method == 'POST':
        print('se quiere enviar algo')
        return redirect('perfilTutorado')
    else:
        print('se va a mostrar algo')
       
        #obtener objetos
        usuario = User.objects.get(id = request.user.id)
        tutorado = Tutorado.objects.get(user_id = request.user.id)

        try:
            padremadretutor = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)
            padremadretutorform = PadreMadreTutorForm(instance = padremadretutor) 
        except:
            padremadretutorform = PadreMadreTutorForm() 

        #autorellenar forms con el instance
        usuarioform = UserForm(instance = usuario)
        perfilTutoradoform = PerfilTutoradoForm(instance = tutorado)

    return render(request, 'editarInformacion.html',{
            'gruops': request.user.groups.all(),
            'title': 'Perfil',
            'cuentaGrupo': cuentaGrupo,
            'formusuario': usuarioform,
            'formPerfilTutorado': perfilTutoradoform,
            'formpadremadretutor': padremadretutorform,
        })

@login_required
@group_required('Tutorado')
def misCitasTutorado(request):
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1
    return render(request, 'miscitas.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ayuda Psicologica',
        'cuentaGrupo': cuentaGrupo
    })

@login_required
@group_required('Tutorado')
def enviarCuestionarioTutorado(request, cuestionario_id):
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        return redirect('paginaInicio')
    else:
        try:
            cuestionario = Cuestionario.objects.get(id = cuestionario_id)
        except:
            return redirect('paginaInicio')
        if tutorado.idGrupo_id == cuestionario.idGrupo_id:
            try:
                respondido = CuestionarioContestado.objects.get(idCuestionario_id = cuestionario.id, idTutorado_id = tutorado.id)
                return redirect('paginaInicio')
            except:
                if request.method == 'GET':
                    cuentaGrupo = 1
                    return render(request, 'enviarCuestionarioTutorado.html', {
                        'gruops': request.user.groups.all(),
                        'title': 'Enviar cuestionario',
                        'cuentaGrupo': cuentaGrupo,
                        'cuestionario': cuestionario,
                        'form': EnviarCuestionario
                    })
                else:
                    form = EnviarCuestionario(request.POST, request.FILES)
                    if form.is_valid():
                        ruta1 = '/static/' + tutorado.idInstitucion.nombreInstitucion + '/' + tutorado.idDepartamentoAcademico.departamentoAcademico + '/' + tutorado.idGrupo.grupo + '/' + str(tutorado.id) + '_' + str(cuestionario_id) + '_' + now().strftime("%Y-%m-%d") + '.pdf'
                        respuesta = guardarArchivo(request.FILES['file'], ruta1)
                        if respuesta:
                            ruta2 = tutorado.idInstitucion.nombreInstitucion + '/' + tutorado.idDepartamentoAcademico.departamentoAcademico + '/' + tutorado.idGrupo.grupo + '/' + str(tutorado.id) + '_' + str(cuestionario_id) + '_' + now().strftime("%Y-%m-%d") + '.pdf'
                            cuestionarioContestado = CuestionarioContestado(ruta = ruta2, idCuestionario_id = cuestionario_id, idTutorado_id = tutorado.id)
                            cuestionarioContestado.save()
                            return redirect('paginaInicio')
                        else:
                            cuentaGrupo = 1
                            return render(request, 'enviarCuestionarioTutorado.html', {
                                'gruops': request.user.groups.all(),
                                'title': 'Enviar cuestionario',
                                'cuentaGrupo': cuentaGrupo,
                                'cuestionario': cuestionario,
                                'form': EnviarCuestionario,
                                'error': 'Error al enviar el archivo, por favor intentelo de nuevo'
                            })
        else:
            return redirect('paginaInicio')

@login_required
@group_required('Tutorado')
def cambiarPassword(request):
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1

    return render(request, 'PerfilTutoradoContra.html',{
        'gruops': request.user.groups.all(),
        'title': 'Cambiar Contraseña',
        'cuentaGrupo': cuentaGrupo
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
