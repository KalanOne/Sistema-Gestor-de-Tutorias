from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import *
from tablib import Dataset 
from django.utils.datastructures import MultiValueDictKeyError
from Tutoria.resources import *
from django.contrib.auth.hashers import make_password
from .documentosModels import *
# Create your views here.

def group_required(*group_names):
    """ Grupos, checar si pertenece a grupo """

    def check(user):
        # if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
        if user.groups.filter(name__in=group_names).exists():
            return True
        else:
            return False
    # Si no se pertenece al grupo, redirigir a pagina principal
    return user_passes_test(check, login_url='inicioSesion')

def pertenece_cualquier_grupo(usuario, lista_grupos):
    return True if usuario.groups.filter(name__in=lista_grupos) else False


@login_required
def cambiarContraseña(request):
    if request.method == 'POST':
        changeform = CambiarPasswordForm(data=request.POST, user=request.user)
        if changeform.is_valid():
            changeform.save()
            update_session_auth_hash(request, changeform.user)
            return redirect('/Inicio')
        else:

            error=True
            changeform = CambiarPasswordForm(user=request.user)
            changeform.fields['old_password'].label = 'Contraseña Actual'
            changeform.fields['new_password1'].label = 'Nueva Contraseña'
            changeform.fields['new_password2'].label = 'Repetir Contraseña'
            return render(request, 'CambiarContra.html', {
                'gruops': request.user.groups.all(),
                'title': 'Cambiar Contraseña',
                'cuentaGrupo': 1,
                'changeform': changeform,
                'error': error
            })
    else:
        
        error=False
        changeform = CambiarPasswordForm(user=request.user)
        changeform.fields['old_password'].label = 'Contraseña Actual'
        changeform.fields['new_password1'].label = 'Nueva Contraseña'
        changeform.fields['new_password2'].label = 'Repetir Contraseña'
        return render(request, 'CambiarContra.html', {
            'gruops': request.user.groups.all(),
            'title': 'Cuestionarios',
            'cuentaGrupo': 1,
            'changeform': changeform,
            'error': error
        })

#Vistas para login, logout y pagina principal para todos los usuarios

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
    elif request.user.groups.filter(name__in=['Psicológico', 'Médico']).exists():
        return render(request, 'paginaInicio.html', {
            'gruops': request.user.groups.all(),
            'title': 'Página de inicio'
        })
    else:
        try:
            personal = PersonalTec.objects.get(user_id = request.user.id)
            if personal.idInstitucion.periodoActual == 2:
                return render(request, 'paginaInicio.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Página de inicio'
                })
            else:
                fechasActuales = FechaLimite.objects.get(ano = personal.idInstitucion.anoActual, periodo = personal.idInstitucion.periodoActual)
                return render(request, 'paginaInicio.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Página de inicio',
                    'fechas': fechasActuales
                })
        except:
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
    hayCuestionarios=False
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        return redirect('paginaInicio')
    fecha = datetime.datetime.now()
    cuestionarios = Cuestionario.objects.filter(idGrupo = tutorado.idGrupo.id, fechaLimite__gte = fecha.strftime("%Y-%m-%d"))
    if cuestionarios.count()>0:
        hayCuestionarios=True

    return render(request, 'cuestionariosTutorado.html', {
        'gruops': request.user.groups.all(),
        'title': 'Cuestionarios',
        'cuentaGrupo': 1,
        'cuestionarios': cuestionarios,
        'haycuestionarios': hayCuestionarios
    })

@login_required
@group_required('Tutorado')
def perfilTutorado(request):
    #obtener objetos
    usuarios = User.objects.get(id = request.user.id)
    usuario=MostrarUserTutoradoForm(instance=usuarios)
    tutorados = Tutorado.objects.get(user_id = request.user.id)
    tutorado=MostrarPerfilTutoradoForm(instance=tutorados)
    departamentoacademicos = DepartamentoAcademico.objects.get(id = tutorados.idDepartamentoAcademico_id)
    departamentoacademico= MostrarDepartamentoAcademicoForm(instance=departamentoacademicos)
    
    if tutorados.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1

    try:
        padremadretutors = PadreMadreTutor.objects.get(id = tutorados.idPadreMadreTutor_id)
        padremadretutor= MostrarPadreMadreForm(instance=padremadretutors)
    except:
        padremadretutor= MostrarPadreMadreForm()
    
    try:
        grupos = Grupo.objects.get(id = tutorados.idGrupo_id)
        grupo= MostrarGrupoForm(instance=grupos)
    except:
        grupo= MostrarGrupoForm()

    for fieldname in usuario.fields:
        usuario.fields[fieldname].disabled = True
    for fieldname in tutorado.fields:
        tutorado.fields[fieldname].disabled = True
    for fieldname in departamentoacademico.fields:
        departamentoacademico.fields[fieldname].disabled = True
    for fieldname in padremadretutor.fields:
        padremadretutor.fields[fieldname].disabled = True
    for fieldname in grupo.fields:
        grupo.fields[fieldname].disabled = True

    return render(request, 'perfilTutorado.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'cuentaGrupo': cuentaGrupo,
        'formusuario': usuario,
        'formPerfilTutorado': tutorado,
        'formpadremadretutor': padremadretutor,
        'formgrupo': grupo,
        'formdepartamentoacademico': departamentoacademico
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
                contestado = 1
                cuentaGrupo = 1
                return render(request, 'enviarCuestionarioTutorado.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Enviar cuestionario',
                    'cuentaGrupo': cuentaGrupo,
                    'cuestionario': cuestionario,
                    'form': EnviarCuestionario(instance = respondido),
                    'contestado' : contestado
                })
            except:
                if request.method == 'GET':
                    cuentaGrupo = 1
                    return render(request, 'enviarCuestionarioTutorado.html', {
                        'gruops': request.user.groups.all(),
                        'title': 'Enviar cuestionario',
                        'cuentaGrupo': cuentaGrupo,
                        'cuestionario': cuestionario,
                        'form': EnviarCuestionario,
                        'contestado' : 0
                    })
                else:
                    form = EnviarCuestionario(request.POST, request.FILES)
                    if form.is_valid():
                        try:
                            modeloEnvio = form.save(commit = False)
                            modeloEnvio.idTutorado_id = tutorado.id
                            modeloEnvio.idCuestionario_id = cuestionario_id
                            modeloEnvio.save()
                            return redirect('paginaInicio')
                        except:
                            cuentaGrupo = 1
                            return render(request, 'enviarCuestionarioTutorado.html', {
                                'gruops': request.user.groups.all(),
                                'title': 'Enviar cuestionario',
                                'cuentaGrupo': cuentaGrupo,
                                'cuestionario': cuestionario,
                                'form': form,
                                'error': 'Error al enviar el archivo, por favor intentelo de nuevo',
                                'contestado' : 0
                            })
                    else:
                        cuentaGrupo = 1
                        return render(request, 'enviarCuestionarioTutorado.html', {
                            'gruops': request.user.groups.all(),
                            'title': 'Enviar cuestionario',
                            'cuentaGrupo': cuentaGrupo,
                            'cuestionario': cuestionario,
                            'form': form,
                            'error': 'Error al enviar el archivo, por favor intentelo de nuevo',
                            'contestado' : 0
                        })
        else:
            return redirect('paginaInicio')

@login_required
@group_required('Tutorado')
def editarInformacion(request):

    if request.method=='GET':
        tutorado = Tutorado.objects.get(user_id = request.user.id)
        usuario = User.objects.get(id = request.user.id)
        usuarioform = EditarUserTutoradoForm(instance = usuario)
        perfilTutoradoform = EditarPerfilTutoradoForm(instance = tutorado)
        try:
            padremadretutor = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)
            padremadretutorform = MostrarPadreMadreForm(instance = padremadretutor) 
        except:
            padremadretutorform = MostrarPadreMadreForm() 

        if tutorado.idGrupo is None:
            cuentaGrupo = 0
        else:
            cuentaGrupo = 1
           
        return render(request, 'editarInformacion.html',{
            'gruops': request.user.groups.all(),
            'title': 'Perfil',
            'cuentaGrupo': cuentaGrupo,
            'formusuario': usuarioform,
            'formPerfilTutorado': perfilTutoradoform,
            'formpadremadretutor': padremadretutorform,
        })
    else:
        tutorado = Tutorado.objects.get(user_id = request.user.id)
        usuario = User.objects.get(id = request.user.id)
        usuarioformpost=EditarUserTutoradoForm(request.POST,instance=usuario)
        perfilTutoradoformpost=EditarPerfilTutoradoForm(request.POST,instance=tutorado)

        if usuarioformpost.is_valid():
            print('usuario valido')
            post=usuarioformpost.save(commit=False)
            post.save()
        else:
            print('usuario no valido')

        try:
            padremadretutorPost = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)
            padremadretutorformpost=EditarPadreMadreForm(request.POST, instance=padremadretutorPost)

            if padremadretutorformpost.is_valid():
                print('tutor valido')
                post=padremadretutorformpost.save(commit=False)
                post.save()
            else:
                print('tutor no valido')

            if perfilTutoradoformpost.is_valid():
                print('tutorado valido')
                post=perfilTutoradoformpost.save(commit=False)
                post.save()
            else:
                print('tutorado no valido')

        except:
            #si no existe el tutor, aqui se crea
            nombre=request.POST['nombre']
            apellidos=request.POST['apellidos']
            telefonotutor=request.POST['telefonotutor']
            pmt=PadreMadreTutor.objects.create(nombre=nombre,apellidos=apellidos,telefonotutor=telefonotutor)

            if perfilTutoradoformpost.is_valid():
                print('tutorado valido 2')
                post=perfilTutoradoformpost.save(commit=False)
                post.idPadreMadreTutor=pmt
                post.save()
            else:
                print('tutorado no valido 2')

        return redirect('perfilTutorado')


@login_required
@group_required('Tutorado')
def misCitasTutorado(request):
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    citasTutorado = Cita.objects.filter(idTutorado_id = tutorado.id).order_by("-id")
    personalMed = PersonalMed.objects.filter(idInstitucion_id = tutorado.idInstitucion_id)
    ordenes = Orden.objects.get(nombreOrden = 'Psicológico')
    motivos = Motivo.objects.filter(idOrden_id = ordenes.id)
    form = SolicitudCitaFormTutorado()
    form.fields['idMotivo'].choices = [(motivo.id, motivo.nombre) for motivo in motivos]
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1
    if request.method == 'GET':
        return render(request, 'miscitas.html',{
            'gruops': request.user.groups.all(),
            'title': 'Ayuda Psicologica',
            'cuentaGrupo': cuentaGrupo,
            'citas': citasTutorado,
            'personalMeds': personalMed,
            'form': form
        })
    else:
        formsolicitud = SolicitudCitaFormTutorado(request.POST)
        if formsolicitud.is_valid():
            try:
                estadosCitas = Estado.objects.get(estado = 'Espera')
                nuevaSolicitud = formsolicitud.save(commit = False)
                nuevaSolicitud.folio = request.user.username + '-' + datetime.datetime.now().strftime("%Y/%m/%d") + '-' + request.user.username
                nuevaSolicitud.idTutorado_id = tutorado.id
                nuevaSolicitud.idOrden_id = ordenes.id
                nuevaSolicitud.idEstado_id = estadosCitas.id
                nuevaSolicitud.idInstitucion_id = tutorado.idInstitucion.id
                nuevaSolicitud.save()
                return render(request, 'miscitas.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Ayuda Psicologica',
                    'cuentaGrupo': cuentaGrupo,
                    'citas': citasTutorado,
                    'personalMeds': personalMed,
                    'form': form,
                    'exito': 'Solicitud creada con éxito'
                })
            except:
                return render(request, 'miscitas.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Ayuda Psicologica',
                    'cuentaGrupo': cuentaGrupo,
                    'citas': citasTutorado,
                    'personalMeds': personalMed,
                    'form': formsolicitud,
                    'error': 'No se ha podido procesar la solicitud'
                })
        else:
            return render(request, 'miscitas.html',{
                'gruops': request.user.groups.all(),
                'title': 'Ayuda Psicologica',
                'cuentaGrupo': cuentaGrupo,
                'citas': citasTutorado,
                'personalMeds': personalMed,
                'form': formsolicitud,
                'error': 'No se ha podido procesar la solicitud'
            })


#vistas para todos los perfiles menos el de tutorado

@login_required
def perfilTodos(request):
    #obtener objetos
    usuarios=User.objects.get(id=request.user.id)
    personaltecs=PersonalTec.objects.get(user_id=request.user.id)
    usuario=MostrarUserTodosForm(instance=usuarios)
    personaltec=MostrarPerfilPersonalTecForm(instance=personaltecs)
    try:
        departamentoacademicos=DepartamentoAcademico.objects.get(id=personaltecs.idDepartamentoAcademico_id)
        departamentoacademico=MostrarDepartamentoAcademicoForm(instance=departamentoacademicos)
    except:
        departamentoacademico=MostrarDepartamentoAcademicoForm()

    for fieldname in usuario.fields:
        usuario.fields[fieldname].disabled = True
    for fieldname in personaltec.fields:
        personaltec.fields[fieldname].disabled = True
    for fieldname in departamentoacademico.fields:
        departamentoacademico.fields[fieldname].disabled = True

    return render(request, 'perfilTodos.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'formusuario': usuario,
        'formperfilPersonalTec': personaltec,
        'formdepartamentoacademico': departamentoacademico
    })

@login_required
def editarInformacionTodos(request):
    #obtener objetos
    if request.method == 'GET':
        usuario=User.objects.get(id=request.user.id)
        personaltec=PersonalTec.objects.get(user_id=request.user.id)

        usuarioform = EditarUserPersonalTecForm(instance = usuario)
        formpersonaltec= EditarPerfilPersonalTecForm(instance=personaltec)


        return render(request, 'editarInformacionTodos.html',{
            'gruops': request.user.groups.all(),
            'title': 'Perfil',
            'formu': usuarioform,
            'formperfilPersonalTec': formpersonaltec,
        })
    
    else:
        usuario=User.objects.get(id=request.user.id)
        personaltec=PersonalTec.objects.get(user_id=request.user.id)

        usuarioform = EditarUserPersonalTecForm(request.POST, instance=usuario)
        formpersonaltec= EditarPerfilPersonalTecForm(request.POST, instance=personaltec)

        if usuarioform.is_valid():
            post=usuarioform.save(commit = False)
            post.save()
        else:
            print('formulario 1 no valido')

        if formpersonaltec.is_valid():
            post2=formpersonaltec.save(commit = False)
            post2.save()
        else:
            print('formulario 2 no valido')

        return redirect('perfilTodos')

@login_required
@group_required('Tutor')
def crearCuestionario(request):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estados = Estado.objects.get(estado = 'Activo')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id, idEstado_id = estados.id)
    form = CrearCuestionarioForm()
    form.fields['idGrupo'].choices = [(grupo.id, grupo.grupo) for grupo in grupos]
    if request.method == 'GET':
        return render(request, 'crear_cuestionario.html',{
            'gruops': request.user.groups.all(),
            'title': 'Crear cuestionario',
            'form': form
        })
    else:
        formCuestionario = CrearCuestionarioForm(request.POST, request.FILES)
        if formCuestionario.is_valid():
            try:
                cuestionarioNuevo = formCuestionario.save(commit = False)
                cuestionarioNuevo.idPersonalTec_id = tutor.id
                cuestionarioNuevo.idEstado_id = estados.id
                cuestionarioNuevo.save()
                return render(request, 'crear_cuestionario.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Crear cuestionario',
                    'form': form,
                    'exito': 'Se ha creado con éxito el cuestionario'
                })
            except:
                return render(request, 'crear_cuestionario.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Crear cuestionario',
                    'form': formCuestionario,
                    'error': 'No se ha podido crear el cuestionario'
                })
        else:
            return render(request, 'crear_cuestionario.html',{
                'gruops': request.user.groups.all(),
                'title': 'Crear cuestionario',
                'form': formCuestionario,
                'error': 'No se ha podido crear el cuestionario'
            })

@login_required
@group_required('Tutor')
def resultadosCuestionarios(request):
    hayResultados=False
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id).exclude(idEstado_id = estadoCerrado.id)

    if grupos.count()>0:
        hayResultados=True

    return render(request, 'Listado_Grupos_Tutor_Cuestionarios.html', {
        'gruops': request.user.groups.all(),
        'title': 'Ver resultados de Cuestionarios',
        'grupos': grupos,
        'hayResultados': hayResultados
    })

@login_required
@group_required('Tutor')
def verResultadosCuestionariosGrupo(request, grupo_id):
    hayCuestionarios=False
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    try:
        grupo = Grupo.objects.get(idPersonalTec_id = tutor.id, id = grupo_id)
    except:
        return redirect('verResultadosCuestionarios')
    tutorados = Tutorado.objects.filter(idGrupo_id = grupo_id)
    cuesitonarios = Cuestionario.objects.filter(idGrupo_id = grupo_id)

    if cuesitonarios.count()>0:
        hayCuestionarios=True

    arr = []
    for cues in cuesitonarios:
       arr.append(cues.id)
    respuestas = CuestionarioContestado.objects.filter(idCuestionario_id__in = arr)

    return render(request, 'resultadosCuestionarios.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ver resultados de Cuestionarios',
        'tutorados': tutorados,
        'cuesitonarios': cuesitonarios,
        'respuestas': respuestas,
        'hayCuestionarios' : hayCuestionarios
    })

@login_required
@group_required('Tutor')
def gruposTutor(request):
    hayGrupos=False
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id).exclude(idEstado_id = estadoCerrado.id)

    if grupos.count()>0:
        hayGrupos=True

    return render(request, 'Listado_Grupos_Tutor_Tutorados.html', {
        'gruops': request.user.groups.all(),
        'title': 'Ver grupos',
        'grupos': grupos,
        'hayGrupos': hayGrupos
    })

@login_required
@group_required('Tutor')
def grupoTutor(request, grupo_id):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    try:
        grupo = Grupo.objects.get(idPersonalTec_id = tutor.id, id = grupo_id)
    except:
        return redirect('gruposTutor')
    tutorados = Tutorado.objects.filter(idGrupo_id = grupo_id)
    return render(request, 'Listado_Tutorados.html', {
        'gruops': request.user.groups.all(),
        'title': 'Ver grupos',
        'tutorados': tutorados,
        'grupo': grupo
    })

@login_required
@group_required('Tutor')
def solicitudPsicologigaTutor(request, grupo_id, tutorado_id):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    try:
        grupo = Grupo.objects.get(idPersonalTec_id = tutor.id, id = grupo_id)
        tutorado = Tutorado.objects.get(idGrupo_id = grupo_id, id = tutorado_id)
    except:
        return redirect('gruposTutor')
    form = SolicitudCitaFormTutor()
    ordenes = Orden.objects.get(nombreOrden = 'Psicológico')
    motivos = Motivo.objects.filter(idOrden_id = ordenes.id)
    form.fields['idMotivo'].choices = [(motivo.id, motivo.nombre) for motivo in motivos]
    
    if request.method == 'GET':
        return render(request, 'Solicitud_Ayuda_Psicologica_Tutor.html', {
            'gruops': request.user.groups.all(),
            'title': 'Solicitar ayuda psicológica',
            'form': form
        })
    else:
        formsolicitud = SolicitudCitaFormTutor(request.POST)
        if formsolicitud.is_valid():
            try:
                estadosCitas = Estado.objects.get(estado = 'Espera')
                nuevaSolicitud = formsolicitud.save(commit = False)
                nuevaSolicitud.folio = request.user.username + '-' + datetime.datetime.now().strftime("%Y/%m/%d") + '-' + tutorado.user.username
                nuevaSolicitud.idTutorado_id = tutorado.id
                nuevaSolicitud.idOrden_id = ordenes.id
                nuevaSolicitud.idEstado_id = estadosCitas.id
                nuevaSolicitud.idPersonalTec_id = tutor.id
                nuevaSolicitud.idInstitucion_id = tutor.idInstitucion.id
                nuevaSolicitud.save()
                return render(request, 'Solicitud_Ayuda_Psicologica_Tutor.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Solicitar ayuda psicológica',
                    'form': form,
                    'exito': 'Solicitud creada con éxito'
                })
            except:
                return render(request, 'Solicitud_Ayuda_Psicologica_Tutor.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Ayuda Psicologica',
                    'form': formsolicitud,
                    'error': 'No se ha podido procesar la solicitud'
                })
        else:
            return render(request, 'miscitas.html',{
                'gruops': request.user.groups.all(),
                'title': 'Ayuda Psicologica',
                'form': formsolicitud,
                'error': 'No se ha podido procesar la solicitud'
            })


# Jefe de Departamento Académico
@login_required
@group_required('Jefe de Departamento Académico','Coordinador de Tutoria del Departamento Académico')
def listaTutor(request):
    if request.method == "GET":
        vacio=0
        try:
            coordinador=PersonalTec.objects.get(user_id=request.user.id)
            tutoresobtener = PersonalTec.objects.filter(idDepartamentoAcademico_id=coordinador.idDepartamentoAcademico_id, idInstitucion_id=coordinador.idInstitucion_id)
            tutores=[]
            for tutor in tutoresobtener:
                if pertenece_cualquier_grupo(tutor.user, ['Tutor']):
                    tutores.append(tutor)
                    vacio=vacio+1
            form=RegistrarPersonalTecForm()
            return render(request, 'listaTutor.html',{
                'gruops': request.user.groups.all(),
                'title': 'Listar Tutores',
                'tutores': tutores,
                'vacio': vacio,
                'form':form
            })
        except:
            vacio=0
            form=RegistrarPersonalTecForm()
            return render(request, 'listaTutor.html',{
                'gruops': request.user.groups.all(),
                'title': 'Listar Tutores',
                'vacio': vacio,
                'form':form
            })
    else:
        vacio=0
        persona_resource = ExcelPersonalTec()
        dataset = Dataset()  
        encargado = PersonalTec.objects.get(user_id = request.user.id)
        escuela = encargado.idInstitucion
        departamento = encargado.idDepartamentoAcademico
        ErrorusuariosExistentes=False
        usuariosExistentes=[]
        try:
            nuevas_personas = request.FILES['archivo']  
        except MultiValueDictKeyError:
            return redirect('listaTutor')
        imported_data = dataset.load(nuevas_personas.read())  
        result = persona_resource.import_data(dataset, dry_run=True)
        
        if not result.has_errors(): 
            persona_resource.import_data(dataset, dry_run=False)
            for tutor in registrarPersonalTec.objects.all():
                if User.objects.filter(username=tutor.username).exists():
                    usuariosExistentes.append(tutor)
                else:
                    try:
                        if tutor.username == "":
                            print("username Vacio")
                        else:
                            password="sgtprofe"+tutor.username
                            usr=User.objects.create(username=tutor.username, password=make_password(password), first_name=tutor.nombres, last_name=tutor.apellidos, email=tutor.email)
                            grupo=Group.objects.get(name="Tutor")
                            usr.groups.add(grupo.id)
                            alm=PersonalTec.objects.create(idDepartamentoAcademico=departamento, idInstitucion=escuela, user=usr)
                            print(tutor.username+"Registro exitoso")
                    except:
                        print("Error no pudo crear el usuario")

            limpiar = registrarPersonalTec.objects.all()         
            limpiar.delete()

            print(len(usuariosExistentes))

            if len(usuariosExistentes)>0:
                ErrorusuariosExistentes=True

            coordinador=PersonalTec.objects.get(user_id=request.user.id)
            tutoresobtener = PersonalTec.objects.filter(idDepartamentoAcademico_id=coordinador.idDepartamentoAcademico_id, idInstitucion_id=coordinador.idInstitucion_id)
            tutores=[]
            for tutor in tutoresobtener:
                if pertenece_cualquier_grupo(tutor.user, ['Tutor']):
                    tutores.append(tutor)
                    vacio=vacio+1
            form=RegistrarPersonalTecForm()

            return render(request, 'listaTutor.html',{
                'gruops': request.user.groups.all(),
                'title': 'Listar Tutores',
                'tutores': tutores,
                'vacio': vacio,
                'form':form,
                'usuarioExiste':usuariosExistentes,
                'Errorusu':ErrorusuariosExistentes
            })

            #return redirect ('listaTutor')
        else:
            print("Error de excel")
            return redirect ('listaTutor')

        return redirect ('listaTutor')


    
@login_required
@group_required('Jefe de Departamento Académico','Coordinador de Tutoria del Departamento Académico')
def crearGrupo(request, Tutor):
    if request.method == 'GET':
        grupoform=GrupoForm()
        estadoActivo = Estado.objects.get(estado = 'Activo')
        estadoInactivo = Estado.objects.get(estado = 'Inactivo')
        elecciones = [
            (estadoActivo.id, estadoActivo.estado),
            (estadoInactivo.id, estadoInactivo.estado)
        ]
        grupoform.fields['idEstado'].choices = elecciones
        return render(request, 'crearGrupo.html', {
            'gruops': request.user.groups.all(),
            'title': 'Crear Grupo',
            'formgrupo': grupoform
        })
    else:
        grupoform=GrupoForm(request.POST)

        if grupoform.is_valid():
            try:
                tutor=PersonalTec.objects.get(id=Tutor)
                post=grupoform.save(commit=False)
                post.grupo=tutor.idDepartamentoAcademico.abreviacion+"-"+str(tutor.idInstitucion.anoActual)+"-"+str(tutor.idInstitucion.periodoActual)+"-"+request.POST['grupo']
                post.idInstitucion_id=tutor.idInstitucion_id
                post.idPersonalTec_id=Tutor
                post.save()
                return redirect('verGruposDelTutor',Tutor)
            except:
                grupoform=GrupoForm()
                return render(request, 'crearGrupo.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Crear Grupo',
                    'formgrupo': grupoform
                })
        else:
            grupoform=GrupoForm()
            return render(request, 'crearGrupo.html', {
                'gruops': request.user.groups.all(),
                'title': 'Crear Grupo',
                'formgrupo': grupoform
            })
        

@login_required
@group_required('Jefe de Departamento Académico','Coordinador de Tutoria del Departamento Académico')
def verGruposDelTutor(request, Tutor):
    if request.method=="GET":
        sobrecargaGrupo=False
        vacio=False
        grupos=Grupo.objects.filter(idPersonalTec_id=Tutor)
        if grupos.count() >= 3:
            sobrecargaGrupo=True

        if grupos.count() == 0:
            vacio=True

        grupoform=GrupoForm()
        estadoActivo = Estado.objects.get(estado = 'Activo')
        estadoInactivo = Estado.objects.get(estado = 'Inactivo')
        elecciones = [
            (estadoActivo.id, estadoActivo.estado),
            (estadoInactivo.id, estadoInactivo.estado)
        ]
        grupoform.fields['idEstado'].choices = elecciones


        return render(request, 'verGrupoDelTutor.html', {
            'gruops': request.user.groups.all(),
            'title': 'Crear Grupo',
            'grupos': grupos,
            'tutor': Tutor,
            'sobrecargaGrupo': sobrecargaGrupo,
            'vacio': vacio,
            'formgrupo': grupoform
        })
    else:
        grupoform=GrupoForm(request.POST)

        if grupoform.is_valid():
            try:
                tutor=PersonalTec.objects.get(id=Tutor)
                post=grupoform.save(commit=False)
                post.grupo=tutor.idDepartamentoAcademico.abreviacion+"-"+str(tutor.idInstitucion.anoActual)+"-"+str(tutor.idInstitucion.periodoActual)+"-"+request.POST['grupo']
                post.idInstitucion_id=tutor.idInstitucion_id
                post.idPersonalTec_id=Tutor
                post.save()
                return redirect('verGruposDelTutor',Tutor)
            except:
                grupoform=GrupoForm()
                return render(request, 'crearGrupo.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Crear Grupo',
                    'grupos': grupos,
                    'tutor': Tutor,
                    'sobrecargaGrupo': sobrecargaGrupo,
                    'vacio': vacio,
                    'formgrupo': grupoform
                })
        else:
            grupoform=GrupoForm()
            return render(request, 'crearGrupo.html', {
                'gruops': request.user.groups.all(),
                'title': 'Crear Grupo',
                'grupos': grupos,
                'tutor': Tutor,
                'sobrecargaGrupo': sobrecargaGrupo,
                'vacio': vacio,
                'formgrupo': grupoform
            })

@login_required
@group_required('Jefe de Departamento Académico','Coordinador de Tutoria del Departamento Académico')
def listarAlumnos(request, Grupoid):
    Error=False
    if request.method == 'GET':
        Error=False
        listaAlumnos=Tutorado.objects.filter(idGrupo_id=Grupoid)
        tieneAlumnos=False
        if listaAlumnos.count() > 0:
            tieneAlumnos=True        
        form=RegistrarTutoradosForm()
        form.fields['archivo'].label = 'Archivo de Alumnos'

        return render(request, 'listarAlumnos.html', {
            'gruops': request.user.groups.all(),
            'title': 'Listar alumnos',
            'lista': listaAlumnos,
            'tieneAlumnos':tieneAlumnos,
            'grupo': Grupoid,
            'form':form,
            'Error':Error
        })
    else:
        Error=False
        numControlError=False
        usuExisteError=False
        persona_resource = ExcelResource()  
        dataset = Dataset()  
        encargado = PersonalTec.objects.get(user_id = request.user.id)
        escuela = encargado.idInstitucion
        departamento = encargado.idDepartamentoAcademico 
        numinvalidos=[]
        usuariosyaexistente=[]

        try:
            nuevas_personas = request.FILES['archivo']  
        except MultiValueDictKeyError:
            return render(request, 'agregarTutorado.html')

        imported_data = dataset.load(nuevas_personas.read())  
        result = persona_resource.import_data(dataset, dry_run=True)

        print(result.has_errors())
        if not result.has_errors():
            persona_resource.import_data(dataset, dry_run=False)
            for Alumno in registrarAlumno.objects.all():
                if User.objects.filter(username=Alumno.control).exists():
                    usuariosyaexistente.append(Alumno)
                else:
                    print("Entro al segundo else")
                    try:
                        try:
                            semestreAlumno=Alumno.semestre
                        except:
                            semestreAlumno=1
                        if Alumno.control == "":
                            print("Num control vacio")
                        else:
                            
                            currentDateTime = datetime.datetime.now()
                            date = currentDateTime.date()
                            year = date.strftime("%y")
                            year=year+"12"
                            if Alumno.control[:4] == year:
                                password="sgttutorado"+Alumno.control
                                usr=User.objects.create(username=Alumno.control, password=make_password(password), first_name=Alumno.nombres, last_name=Alumno.apellidos, email=Alumno.email)
                                grupo=Group.objects.get(name="Tutorado")
                                usr.groups.add(grupo.id)
                                alm=Tutorado.objects.create(semestre=semestreAlumno,idGrupo_id=Grupoid, idDepartamentoAcademico=departamento, idInstitucion=escuela, user=usr)
                                print(Alumno.control+"Registro exitoso") 
                            else:
                               numinvalidos.append(Alumno)
                             
                    except:
                        print("Erro no pudo crear el usuario")
            limpiar = registrarAlumno.objects.all()         
            limpiar.delete()

            if len(numinvalidos)>0:
                numControlError=True
            if len(usuariosyaexistente)>0:
                usuExisteError=True

            Error=False
            listaAlumnos=Tutorado.objects.filter(idGrupo_id=Grupoid)
            tieneAlumnos=False
            if listaAlumnos.count() > 0:
                tieneAlumnos=True        
            form=RegistrarTutoradosForm()
            form.fields['archivo'].label = 'Archivo de Alumnos'
            return render(request, 'listarAlumnos.html', {
                'gruops': request.user.groups.all(),
                'title': 'Listar alumnos',
                'lista': listaAlumnos,
                'tieneAlumnos':tieneAlumnos,
                'grupo': Grupoid,
                'form':form,
                'Error':Error,
                'numControl':numinvalidos,
                'Errornum':numControlError,
                'usuarioExiste': usuariosyaexistente,
                'Errorusu':usuExisteError
            })
            #return redirect ('listarAlumnos',Grupoid)
        else:
            print("Error") 
            return redirect ('listarAlumnos',Grupoid)

# Coordinador de Tutoria del Departamento Académico

# @login_required
# @group_required('Jefe de Departamento Académico')
# def registrarTutorados(request, Grupoid):  
#     Error=False
#     if request.method == 'POST':  
#         persona_resource = ExcelResource()  
#         dataset = Dataset()  
#         encargado = PersonalTec.objects.get(user_id = request.user.id)
#         escuela = encargado.idInstitucion
#         departamento = encargado.idDepartamentoAcademico 

#         try:
#             nuevas_personas = request.FILES['archivo']  
#         except MultiValueDictKeyError:
#             return render(request, 'agregarTutorado.html')

#         imported_data = dataset.load(nuevas_personas.read())  
#         result = persona_resource.import_data(dataset, dry_run=True)

#         if not result.has_errors(): 
#             persona_resource.import_data(dataset, dry_run=False) # Actually import now  
#             for Alumno in registrarAlumno.objects.all():
#                 if User.objects.filter(username=Alumno.control).exists():
#                     print(Alumno.control+" - Usuario ya existente")
#                 else:
#                     try:
#                         try:
#                             semestreAlumno=Alumno.semestre
#                         except:
#                             semestreAlumno=1
#                         usr=User.objects.create(username=Alumno.control, password=make_password(Alumno.email), first_name=Alumno.nombres, last_name=Alumno.apellidos, email=(Alumno.control+"@morelia.tecnm.mx"))
#                         usr.groups.add(1)
#                         alm=Tutorado.objects.create(semestre=semestreAlumno,idGrupo_id=Grupoid, idDepartamentoAcademico=departamento, idInstitucion=escuela, user=usr)
#                         print("Registro exitoso")  
#                     except:
#                         print("Erro no pudo crear el usuario")

#             limpiar = registrarAlumno.objects.all()         
#             limpiar.delete()

            
#             return redirect ('listarAlumnos',Grupoid)
#         else:
#             print("Error") 
#             Error=True
#             form=RegistrarTutoradosForm()
#             form.fields['archivo'].label = 'Archivo de Alumnos'
#             return render(request, 'agregarTutorado.html',{
#                 'gruops': request.user.groups.all(),
#                 'form':form,
#                 'Error':Error
#             })
#     else:
#         Error=False
#         form=RegistrarTutoradosForm()
#         form.fields['archivo'].label = 'Archivo de Alumnos'
#         return render(request, 'agregarTutorado.html',{
#             'gruops': request.user.groups.all(),
#             'form':form,
#             'Error':Error
#         })

#vista subir credito
@login_required
@group_required('Tutorado')
def subir_credito(request):
    tutorado=Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1
    if request.method == 'POST':  
        form=SubirCreditoForm(request.POST, request.FILES)
        if form.is_valid():
            print("es valido")
            estado=Estado.objects.get(estado='Espera')
            nuevoCredito = form.save(commit = False)
            nuevoCredito.idEstado=estado
            nuevoCredito.idTutorado=tutorado
            nuevoCredito.save()
            print("Guardaddo")
        else:
            print("no es valido")
        return redirect('ver_credito_tutorado')
    else:
        form=SubirCreditoForm()
        return render(request, 'subir_credito.html',{
            'gruops': request.user.groups.all(),
            'cuentaGrupo': cuentaGrupo,
            'title': 'Creditos complementarios',
            'form':form
        })

#vista editar credito
@login_required
@group_required('Tutorado')
def editar_credito(request, dato):
    tutorado=Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1
    if request.method == 'POST':  
        credito=Credito.objects.get(id=dato)
        form=SubirCreditoForm(request.POST, request.FILES, instance=credito)
        estado=Estado.objects.get(estado='Espera')
        if form.is_valid():
            print("es valido")
            editaCredito = form.save(commit = False)
            editaCredito.idEstado=estado
            editaCredito.save()
        else:
            print("no es valido") 
        return redirect ('ver_credito_tutorado')
    else:
        form=SubirCreditoForm()
        return render(request, 'editar_credito.html',{
            'gruops': request.user.groups.all(),
            'cuentaGrupo': cuentaGrupo,
            'title': 'Creditos complementarios',
            'form':form
        })


#vista revisar credito
@login_required
@group_required('Encargado de Créditos Complementarios')
def revisar_credito(request, dato):
    
    if request.method == 'POST':  
        creditoActual= Credito.objects.get(id=dato)
        form=DecisionCreditoForm(request.POST,instance=creditoActual)
        if form.is_valid():
            print('es valido')
            editaCredito = form.save(commit = False)
            editaCredito.save()
        
        return redirect ('ver_credito_tutor')
    else:
        form=DecisionCreditoForm()
        estadoAceptado = Estado.objects.get(estado = 'Aceptado')
        estadoRechazado = Estado.objects.get(estado = 'Rechazado')
        elecciones = [
            (estadoAceptado.id, estadoAceptado.estado),
            (estadoRechazado.id, estadoRechazado.estado)
        ]
        form.fields['idEstado'].choices = elecciones
        return render(request, 'revisar_credito.html',{
            'gruops': request.user.groups.all(),
            'title': 'Creditos complementarios',
            'form':form
        })


#Vista ver creditos tutorado
@login_required
@group_required('Tutorado')
def ver_credito_tutorado(request):    
    tutorado=Tutorado.objects.get(user_id = request.user.id)
    nocredito=False

    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1

    creditos=Credito.objects.filter(idTutorado = tutorado)
    if creditos.count()==0:
        nocredito=True
    return render(request, 'ver_credito_tutorado.html', {
        'gruops': request.user.groups.all(),
        'cuentaGrupo': cuentaGrupo,
        'title': 'Ver creditos',
        'Credito': creditos,
        'Nocredito':nocredito
    })


#Vista ver creditos encargado
@login_required
@group_required('Encargado de Créditos Complementarios')
def ver_credito_tutor(request):
    nocreditos=False
    encargado = PersonalTec.objects.get(user_id = request.user.id)
    alumnos = Tutorado.objects.filter(idDepartamentoAcademico = encargado.idDepartamentoAcademico.id).values('id')
    estado= Estado.objects.get(estado='Espera')
    credito=Credito.objects.filter(idTutorado__in = alumnos, idEstado =estado )
    if credito.count()==0:
        nocreditos=True

    return render(request, 'ver_credito_tutor.html', {
        'gruops': request.user.groups.all(),
        'title': 'Revisar creditos',
        'Credito': credito,
        'nocreditos':nocreditos
    })

@login_required
@group_required('Subdirector Académico')
def registrarJefeDesarrolloAca(request):

    if request.method=="GET":
        form=RegistrarUserForm()
        return render(request, 'registrarJefeDesarrolloAca.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Jefe de Desarrollo Academico',
            'form': form
        })
    else:
        form=RegistrarUserForm(request.POST)
        if form.is_valid():
            postform=form.save(commit=False)
            password="sgtjefedesarrollo"+postform.username
            postform.password= make_password(password)
            postform.save()
            print('valido form')
        else:
            return render(request, 'registrarJefeDesarrolloAca.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Jefe de Desarrollo Academico',
                'form': form
            })

        try:
            next_usr = User.objects.order_by('-id').first().id
        except:
            next_usr = 1

        usr = PersonalTec.objects.get(user_id = request.user.id)
        usr2= User.objects.get(id=next_usr)
        grupo=Group.objects.get(name="Jefe de Desarrollo Académico")
        usr2.groups.add(grupo.id)
        PersonalTec.objects.create(idInstitucion=usr.idInstitucion, user=usr2)

        return redirect('/Inicio')


@login_required
@group_required('Subdirector Académico')
def registrarCoordinacionInstitucional(request):

    if request.method=="GET":
        form=RegistrarUserForm()
        return render(request, 'registrarCoordinacionInstitucional.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Coordinación Institucional de Tutoría',
            'form': form
        })
    else:
        form=RegistrarUserForm(request.POST)
        if form.is_valid():
            postform=form.save(commit=False)
            password="sgtcoordinacioninstitucional"+postform.username
            postform.password= make_password(password)
            postform.save()
            print('valido form')
        else:
            return render(request, 'registrarCoordinacionInstitucional.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Coordinación Institucional de Tutoría',
                'form': form
            })

        try:
            next_usr = User.objects.order_by('-id').first().id
        except:
            next_usr = 1

        usr = PersonalTec.objects.get(user_id = request.user.id)
        usr2= User.objects.get(id=next_usr)
        grupo=Group.objects.get(name="Coordinación Institucional de Tutoría")
        usr2.groups.add(grupo.id)
        PersonalTec.objects.create(idInstitucion=usr.idInstitucion, user=usr2)

        return redirect('/Inicio')
    


@login_required
@group_required('Jefe de Desarrollo Académico')
def registrarJefeDepartamentoAcademico(request):

    if request.method=="GET":
        Existen=False
        form=RegistrarUserForm()
        formpersonal=RegistrarPersonalTecForm2()
        jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
        usuarios=User.objects.filter(groups__name='Jefe de Departamento Académico')
        jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
        if(jefes.count()>0):
            Existen=True

        return render(request, 'registrarJefeDepartamento.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Jefe de Departamento Académico',
            'form': form,
            'formpersonal': formpersonal,
            'jefes':jefes,
            'existe':Existen
        })
    else:
        form=RegistrarUserForm(request.POST)
        formpersonal=RegistrarPersonalTecForm2(request.POST)
        if form.is_valid():
            postform=form.save(commit=False)
            password="sgtjefedepartamento"+postform.username
            postform.password= make_password(password)
            postform.save()
            print('valido form')
        else:
            Existen=False
            jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
            usuarios=User.objects.filter(groups__name='Jefe de Departamento Académico')
            jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
            if(jefes.count()>0):
                Existen=True
            return render(request, 'registrarJefeDepartamento.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Jefe de Departamento Académico',
                'form': form,
                'formpersonal': formpersonal,
                'jefes':jefes,
                'existe':Existen
            })

        if formpersonal.is_valid():
            try:
                next_usr = User.objects.order_by('-id').first().id
            except:
                next_usr = 1
            usr = PersonalTec.objects.get(user_id = request.user.id)
            usr2= User.objects.get(id=next_usr)
            postformpersonal=formpersonal.save(commit=False)
            postformpersonal.idInstitucion= usr.idInstitucion
            postformpersonal.user=usr2
            grupo=Group.objects.get(name="Jefe de Departamento Académico")
            usr2.groups.add(grupo.id)
            postformpersonal.save()
            print('valido formpersonal')
        else:
            Existen=False
            jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
            usuarios=User.objects.filter(groups__name='Jefe de Departamento Académico')
            jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
            if(jefes.count()>0):
                Existen=True
            return render(request, 'registrarJefeDepartamento.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Jefe de Departamento Académico',
                'form': form,
                'formpersonal': formpersonal,
                'jefes':jefes,
                'existe':Existen
            })

        Existen=False
        form=RegistrarUserForm()
        formpersonal=RegistrarPersonalTecForm2()
        jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
        usuarios=User.objects.filter(groups__name='Jefe de Departamento Académico')
        jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
        if(jefes.count()>0):
            Existen=True

        return render(request, 'registrarJefeDepartamento.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Jefe de Departamento Académico',
            'form': form,
            'formpersonal': formpersonal,
            'jefes':jefes,
            'existe':Existen
        })


@login_required
@group_required('Coordinación Institucional de Tutoría')
def registrarCoordinadorTutoria(request):

    if request.method=="GET":
        Existen=False
        form=RegistrarUserForm()
        formpersonal=RegistrarPersonalTecForm2()
        jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
        usuarios=User.objects.filter(groups__name='Coordinador de Tutoria del Departamento Académico')
        jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
        if(jefes.count()>0):
            Existen=True

        return render(request, 'registrarCoordinadorTutoria.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Coordinador de Tutoria del Departamento Académico',
            'form': form,
            'formpersonal': formpersonal,
            'jefes':jefes,
            'existe':Existen
        })
    else:
        form=RegistrarUserForm(request.POST)
        formpersonal=RegistrarPersonalTecForm2(request.POST)
        if form.is_valid():
            postform=form.save(commit=False)
            password="sgtcoordinadortutoria"+postform.username
            postform.password= make_password(password)
            postform.save()
            print('valido form')
        else:
            Existen=False
            jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
            usuarios=User.objects.filter(groups__name='Coordinador de Tutoria del Departamento Académico')
            jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
            if(jefes.count()>0):
                Existen=True
            return render(request, 'registrarCoordinadorTutoria.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Coordinador de Tutoria del Departamento Académico',
                'form': form,
                'formpersonal': formpersonal,
                'jefes':jefes,
                'existe':Existen
            })

        if formpersonal.is_valid():
            try:
                next_usr = User.objects.order_by('-id').first().id
            except:
                next_usr = 1
            usr = PersonalTec.objects.get(user_id = request.user.id)
            usr2= User.objects.get(id=next_usr)
            postformpersonal=formpersonal.save(commit=False)
            postformpersonal.idInstitucion= usr.idInstitucion
            postformpersonal.user=usr2
            grupo=Group.objects.get(name="Coordinador de Tutoria del Departamento Académico")
            usr2.groups.add(grupo.id)
            postformpersonal.save()
            print('valido formpersonal')
        else:
            Existen=False
            jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
            usuarios=User.objects.filter(groups__name='Coordinador de Tutoria del Departamento Académico')
            jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
            if(jefes.count()>0):
                Existen=True
            return render(request, 'registrarCoordinadorTutoria.html', {
                'gruops': request.user.groups.all(),
                'title': 'Registrar Coordinador de Tutoria del Departamento Académico',
                'form': form,
                'formpersonal': formpersonal,
                'jefes':jefes,
                'existe':Existen
            })

        Existen=False
        form=RegistrarUserForm()
        formpersonal=RegistrarPersonalTecForm2()
        jefeDesarrollo=PersonalTec.objects.get(user_id=request.user.id)
        usuarios=User.objects.filter(groups__name='Coordinador de Tutoria del Departamento Académico')
        jefes=PersonalTec.objects.filter(user__in = usuarios, idInstitucion=jefeDesarrollo.idInstitucion)
        if(jefes.count()>0):
            Existen=True

        return render(request, 'registrarCoordinadorTutoria.html', {
            'gruops': request.user.groups.all(),
            'title': 'Registrar Coordinador de Tutoria del Departamento Académico',
            'form': form,
            'formpersonal': formpersonal,
            'jefes':jefes,
            'existe':Existen
        })

@login_required
@group_required('Coordinación Institucional de Tutoría', 'Jefe de Desarrollo Académico', 'Subdirector Académico')
def listado_Personal(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    grupos = []
    personal = PersonalMed.objects.filter(idInstitucion_id = coordinador.idInstitucion.id)  
    personal2 = PersonalTec.objects.filter(idInstitucion_id = coordinador.idInstitucion.id)

    for p in personal:
        for a in p.user.groups.all():
            grupos.append({"id": p.user.id, "puesto": a})

    for p in personal2:
        for a in p.user.groups.all():
            grupos.append({"id": p.user.id, "puesto": a})
    
    # for p in grupos:
    #     print(p)

    return render(request, 'listado_Personal.html', {
        'gruops': request.user.groups.all(),
        'title': 'Personal',
        'personal': personal,
        'personal2': personal2,
        'grupitosUser': grupos
    })

@login_required
@group_required('Tutor')
def VisualizarConstanciaTutor(request):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    constancias = ConstanciaTutorV2.objects.filter(tutor_id = tutor.id)

    return render(request, 'SistemaDeDocumentos/Tutor_VisualizarCosntancia.html', {
        'gruops': request.user.groups.all(),
        'title': 'Constancias',
        'constancias': constancias
    })

@login_required
@group_required('Subdirector Académico','Jefe de Desarrollo Académico','Coordinación Institucional de Tutoría')
def crearDepartamento(request):
    if request.method=='GET':
        form=CrearDepartamentoForm()
        return render(request,'crearDepartamento.html',{
            'gruops': request.user.groups.all(),
            'title': 'Crear Departamento Académico',
            'form':form
        })
    else:
        noError=False
        usr=PersonalTec.objects.get(user=request.user.id)
        form=CrearDepartamentoForm(request.POST)
        if form.is_valid:
            post=form.save(commit=False)
            post.idInstitucion=usr.idInstitucion
            form.save()
            noError=True
        else:
            noError=False
        
        form=CrearDepartamentoForm()
        return render(request,'crearDepartamento.html',{
            'gruops': request.user.groups.all(),
            'title': 'Crear Departamento Académico',
            'form': form,
            'Error': noError
        })
