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
        # if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
        if user.groups.filter(name__in=group_names).exists():
            return True
        else:
            return False
    # Si no se pertenece al grupo, redirigir a pagina principal
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
    #obtener tutorado
    tutorado = Tutorado.objects.get(user_id = request.user.id)
    if tutorado.idGrupo is None:
        cuentaGrupo = 0
    else:
        cuentaGrupo = 1
           
    #obtener objetos
    usuario = User.objects.get(id = request.user.id)
    tutorado = Tutorado.objects.get(user_id = request.user.id)

    #crear formulario de padremadretutor si existe o no
    try:
        padremadretutor = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)
        padremadretutorform = PadreMadreTutorForm(instance = padremadretutor) 
    except:
        padremadretutorform = PadreMadreTutorForm() 

    #autorellenar forms con el instance
    usuarioform = UserForm(instance = usuario)
    perfilTutoradoform = PerfilTutoradoForm(instance = tutorado)
    
    #acciones para cuando se mande el form
    if request.method == 'POST':
        
        #se crean formularios con los datos que ya tiene para despues solo modificar los que se manda por post
        usuarioformpost=UserForm()
        usuarioformpost=usuarioform
        perfilTutoradoformpost=PerfilTutoradoForm()
        perfilTutoradoformpost=perfilTutoradoform

        #valida si el form que se lleno anteriormente es valido y se modifican los valores recibido en post
        if usuarioformpost.is_valid:
            post=usuarioformpost.save(commit=False)
            post.first_name=request.POST['first_name']
            post.last_name=request.POST['last_name']
            post.save()
            
        try:
            #se intenta obtener el objeto PadreMadreTutor para saber si existe o no
            padremadretutorPost = PadreMadreTutor.objects.get(id = tutorado.idPadreMadreTutor_id)

            padremadretutorformpost=PadreMadreTutorForm() 
            padremadretutorformpost=padremadretutorform

            #valida si el form que se lleno anteriormente es valido y se modifican los valores recibido en post
            if padremadretutorformpost.is_valid:
                post=padremadretutorformpost.save(commit=False)
                post.nombre=request.POST['nombre']
                post.apellidos=request.POST['apellidos']
                post.telefonotutor=request.POST['telefonotutor']
                post.save()

            #valida si el form que se lleno anteriormente es valido y se modifican los valores recibido en post
            if perfilTutoradoformpost.is_valid:
                post=perfilTutoradoformpost.save(commit=False)
                post.domicilio=request.POST['domicilio']
                post.telefono=request.POST['telefono']
                post.correoPersonal=request.POST['correoPersonal']
                post.save()
        except:
            #obtenemos id del siguiente tutor que se va a registrar
            try:
                next_tutor = PadreMadreTutor.objects.order_by('-id').first().id + 1
            except:
                next_tutor=1
            
            #obtenemos datos del formulario para despues registrar un nuevo tutor
            nombre=request.POST['nombre']
            apellidos=request.POST['apellidos']
            telefonotutor=request.POST['telefonotutor']
            pmt=PadreMadreTutor.objects.create(nombre=nombre,apellidos=apellidos,telefonotutor=telefonotutor)

            #valida si el form que se lleno anteriormente es valido y se modifican los valores recibido en post
            if perfilTutoradoformpost.is_valid:
                post=perfilTutoradoformpost.save(commit=False)
                post.domicilio=request.POST['domicilio']
                post.telefono=request.POST['telefono']
                post.correoPersonal=request.POST['correoPersonal']
                post.idPadreMadreTutor_id=next_tutor
                post.save()

        return redirect('perfilTutorado')
    
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
    citasTutorado = Cita.objects.filter(idTutorado_id = tutorado.id)
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
    for fieldname in usuarioform.fields:
        usuarioform.fields[fieldname].disabled = True

    perfilPersonalTecform=PerfilPersonalTecForm(instance=personaltec)
    for fieldname in perfilPersonalTecform.fields:
        perfilPersonalTecform.fields[fieldname].disabled = True

    departamentoacademicoform=DepartamentoAcademicoForm(instance=departamentoacademico)
    for fieldname in departamentoacademicoform.fields:
        departamentoacademicoform.fields[fieldname].disabled = True

    return render(request, 'perfilTodos.html',{
        'gruops': request.user.groups.all(),
        'title': 'Perfil',
        'formusuario': usuarioform,
        'formperfilPersonalTec': perfilPersonalTecform,
        'formdepartamentoacademico': departamentoacademicoform
    })

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
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id).exclude(idEstado_id = estadoCerrado.id)
    return render(request, 'Listado_Grupos_Tutor_Cuestionarios.html', {
        'gruops': request.user.groups.all(),
        'title': 'Ver resultados de Cuestionarios',
        'grupos': grupos
    })

@login_required
@group_required('Tutor')
def verResultadosCuestionariosGrupo(request, grupo_id):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    try:
        grupo = Grupo.objects.get(idPersonalTec_id = tutor.id, id = grupo_id)
    except:
        return redirect('verResultadosCuestionarios')
    tutorados = Tutorado.objects.filter(idGrupo_id = grupo_id)
    cuesitonarios = Cuestionario.objects.filter(idGrupo_id = grupo_id)
    arr = []
    for cues in cuesitonarios:
       arr.append(cues.id)
    respuestas = CuestionarioContestado.objects.filter(idCuestionario_id__in = arr)

    return render(request, 'resultadosCuestionarios.html',{
        'gruops': request.user.groups.all(),
        'title': 'Ver resultados de Cuestionarios',
        'tutorados': tutorados,
        'cuesitonarios': cuesitonarios,
        'respuestas': respuestas
    })

@login_required
@group_required('Tutor')
def gruposTutor(request):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id).exclude(idEstado_id = estadoCerrado.id)
    return render(request, 'Listado_Grupos_Tutor_Tutorados.html', {
        'gruops': request.user.groups.all(),
        'title': 'Ver grupos',
        'grupos': grupos
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


# Coordinador de Tutoria del Departamento Académico
@login_required
@group_required('Coordinador de Tutoria del Departamento Académico')
def listaTutor(request):
    try:
        coordinador=get_object_or_404(PersonalTec, user_id=request.user.id)
        tutores = PersonalTec.objects.filter(idDepartamentoAcademico_id=coordinador.idDepartamentoAcademico_id, idInstitucion_id=coordinador.idInstitucion_id)
        lista=[]
        lista_tutor=[]
        for tutor in tutores:
            usuario=get_object_or_404(User, id=tutor.user_id)
            if usuario.groups.filter(name__in=['Tutor']):
                lista=[tutor,usuario]
                lista_tutor.append(lista)

        return render(request, 'listaTutor.html',{
            'gruops': request.user.groups.all(),
            'title': 'Listar Tutores',
            'tutores': lista_tutor,
        })

    except:
        return render(request, 'listaTutor.html',{
            'gruops': request.user.groups.all(),
            'title': 'Listar Tutores'
        })

    
@login_required
@group_required('Coordinador de Tutoria del Departamento Académico')
def crearGrupo(request, Tutor):
    if request.method == 'GET':
        grupoform=GrupoForm()
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
                post.grupo="ISC-"+request.POST['grupo']
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
@group_required('Coordinador de Tutoria del Departamento Académico')
def verGruposDelTutor(request, Tutor):
    print(Tutor)
    grupos=Grupo.objects.filter(idPersonalTec_id=Tutor)
    return render(request, 'verGrupoDelTutor.html', {
        'gruops': request.user.groups.all(),
        'title': 'Crear Grupo',
        'grupos': grupos,
        'tutor':Tutor
    })

@login_required
@group_required('Coordinador de Tutoria del Departamento Académico')
def listarAlumnos(request, Grupoid):

    if request.method == 'GET':
        listaAlumnos=Tutorado.objects.filter(idGrupo_id=Grupoid)
        tieneAlumnos=False
        lista=[]
        listaTutorado=[]
        if listaAlumnos.count() > 0:
            tieneAlumnos=True
            for alumno in listaAlumnos:
                usuario=get_object_or_404(User, id=alumno.user_id)
                lista=[alumno,usuario]
                listaTutorado.append(lista)         

        return render(request, 'listarAlumnos.html', {
            'gruops': request.user.groups.all(),
            'title': 'Listar alumnos',
            'lista': listaTutorado,
            'tieneAlumnos':tieneAlumnos
        })

#pruebas
@login_required
@group_required('Tutor', 'Tutorado')
def prueba(request):
    return render(request, 'prueba.html', {
        'groups': request.user.groups.all()
    })
