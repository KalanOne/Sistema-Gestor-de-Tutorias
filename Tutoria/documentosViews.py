from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
import datetime
from django.contrib.auth.models import User
from .documentosForms import *
from .documentosModels import *
from django.forms import modelformset_factory
from django.db import transaction
from docxtpl import *
from docx2pdf import *
from PyPDF2 import *
from datetime import date
from datetime import datetime
import pythoncom

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
@group_required('Tutor')
def SelectGruposReporteSemestral(request):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    grupos = Grupo.objects.filter(idPersonalTec_id = tutor.id).exclude(idEstado_id = estadoCerrado.id)
    reportes = ReporteSemestralGrupalV2.objects.filter(grupo__in = grupos, ano = tutor.idInstitucion.anoActual, periodo = tutor.idInstitucion.periodoActual)
    return render(request, 'SistemaDeDocumentos/Tutor_SelectGruposReporteSemestral.html', {
        'gruops': request.user.groups.all(),
        'title': 'Seleccionar Grupos Para Reporte Semestral',
        'tutor': tutor,
        'grupos': grupos,
        'reportes': reportes
    })

@login_required()
@group_required('Tutor')
def VisualizarReportesSemestralesGrupalesTutor(request):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    reportes = ReporteSemestralGrupalV2.objects.filter(tutor_id = tutor.id)
    return render(request, 'SistemaDeDocumentos/Tutor_VisualizarReportesSemestralesGrupalesTutor.html', {
        'gruops': request.user.groups.all(),
        'title': 'Seleccionar Grupos Para Reporte Semestral',
        'tutor': tutor,
        'reportes': reportes
    })

@login_required()
@group_required('Tutor')
@transaction.atomic
def CrearReporteSemestralGrupal(request, grupo_id):
    tutor = PersonalTec.objects.get(user_id = request.user.id)
    try:
        grupo = Grupo.objects.get(id = grupo_id, idPersonalTec_id = tutor.id)
    except:
        return redirect('inicioSesion')
    
    try:
        reporte = ReporteSemestralGrupalV2.objects.get(ano = tutor.idInstitucion.anoActual, periodo = tutor.idInstitucion.periodoActual, grupo_id = grupo_id, tutor_id = tutor.id)
        return render(request, 'SistemaDeDocumentos/Tutor_CrearReporteSemestralGrupal.html',{
            'gruops': request.user.groups.all(),
            'title': 'Seleccionar Grupos Para Reporte Semestral',
            'tutor': tutor,
            'reporte': reporte,
            'realizado': 1
        })
    except:
        pass
    
    tutorados = Tutorado.objects.filter(idGrupo_id = grupo_id)
    noTutorados = tutorados.count()
    formularios = modelformset_factory(TutoradoReporteSemestralGrupalV2, form = FormTutoradoReporteSemestralGrupalCreditoV2, extra = noTutorados)
    
    if request.method == 'GET':
        formularios2 = formularios()
        for indice, form in enumerate(formularios2):
            ele = [(tutorados[indice].id, tutorados[indice])]
            form.fields['tutorado'].choices = ele
        return render(request, 'SistemaDeDocumentos/Tutor_CrearReporteSemestralGrupal.html',{
            'gruops': request.user.groups.all(),
            'title': 'Seleccionar Grupos Para Reporte Semestral',
            'tutor': tutor,
            'realizado': 0,
            'form': formularios2
        })
    else:
        formularios2 = formularios(request.POST)
        if formularios2.is_valid():
            # try:
            instancias = formularios2.save(commit = False)
            estadoAceptado = Estado.objects.get(estado = 'Aceptado')
            reporteGrupal = ReporteSemestralGrupalV2()
            reporteGrupal.ano = tutor.idInstitucion.anoActual
            reporteGrupal.periodo = tutor.idInstitucion.periodoActual
            reporteGrupal.grupo_id = grupo_id
            reporteGrupal.tutor_id = tutor.id
            reporteGrupal.estado_id = estadoAceptado.id
            reporteGrupal.save()
            for item in instancias:
                item.reporte_id = reporteGrupal.id
                item.save()
            
            ahora = datetime.now()

            coordTutoDeptAcade = PersonalTec.objects.filter(idDepartamentoAcademico_id = tutor.idDepartamentoAcademico.id)
            coordTutoDeptAcade2 = []
            for coor in coordTutoDeptAcade:
                if pertenece_cualquier_grupo(coor.user, ['Coordinador de Tutoria del Departamento Académico']):
                    coordTutoDeptAcade2.append(coor)
            
            jefeDeptAcade2 = []
            for coor in coordTutoDeptAcade:
                if pertenece_cualquier_grupo(coor.user, ['Jefe de Departamento Académico']):
                    jefeDeptAcade2.append(coor)

            context = {
                'departamento': tutor.idDepartamentoAcademico.departamentoAcademico,
                'tutor': tutor.user.first_name + ' ' + tutor.user.last_name,
                'fecha': ahora.strftime("%d/%m/%Y"),
                'hora': ahora.strftime("%H:%M:%S"),
                'nombreGrupo': grupo.grupo,
                'tutoradosInfo': instancias,
                'coordTutoDeptAcade': coordTutoDeptAcade2[0].user,
                'jefeDeptAcade': jefeDeptAcade2[0].user
            }

            templateReporte = DocxTemplate("Tutoria/static/Templates/Template_ReporteSemestralGrupalTutor.docx")
            nombre = tutor.user.username + "ReporteSemestralGrupal" + ahora.strftime("__%d_%m_%Y_%H_%M_%S")
            inicioRuta = "Tutoria/static/borrar/"
            inicioRutaReporte = "Tutoria/static/Archivos/Reportes/"
            templateReporte.render(context)
            templateReporte.save(inicioRuta + nombre + ".docx")
            pythoncom.CoInitialize()
            convert(inicioRuta + nombre + ".docx", inicioRutaReporte + nombre + ".pdf")

            estadoActivo = Estado.objects.get(estado = 'Activo')
            if grupo.idEstado_id == estadoActivo.id:
                for est in instancias:
                    if est.credito == True or est.credito == 1:
                        templateCredito = DocxTemplate("Tutoria/static/Templates/Template_ConstanciaTutorado.docx")
                        nombreCredito = est.tutorado.user.username + "CreditoComplementario" + ahora.strftime("__%d_%m_%Y_%H_%M_%S")
                        inicioRutaCredito = "Tutoria/static/Archivos/Creditos/"
                        context2 = {
                            'tutorado': est.tutorado.user.first_name + est.tutorado.user.last_name
                        }
                        templateCredito.render(context2)
                        templateCredito.save(inicioRuta + nombreCredito + ".docx")
                        convert(inicioRuta + nombreCredito + ".docx", inicioRutaCredito + nombreCredito + ".pdf")
            
            templateConst = DocxTemplate("Tutoria/static/Templates/Template_ConstanciaTutor.docx")
            nombreConst = tutor.user.username + "Constancia" + ahora.strftime("__%d_%m_%Y_%H_%M_%S")
            inicioRutaConst = "Tutoria/static/Archivos/Constancias/"
            context3 = {
                'tutor': tutor.user.first_name + tutor.user.last_name,
                'grupo': grupo.grupo
            }
            templateConst.render(context3)
            templateConst.save(inicioRuta + nombreConst + ".docx")
            convert(inicioRuta + nombreConst + ".docx", inicioRutaConst + nombreConst + ".pdf")


            reporteGrupal.archivo = "Archivos/Reportes/" + nombre + ".pdf"
            reporteGrupal.save()

            constancia = ConstanciaTutorV2()
            constancia.archivo = "Archivos/Constancias/" + nombreConst + ".pdf"
            constancia.ano = tutor.idInstitucion.anoActual
            constancia.periodo = tutor.idInstitucion.periodoActual
            constancia.grupo_id = grupo_id
            constancia.tutor_id = tutor.id
            constancia.estado_id = estadoAceptado.id
            constancia.save()

            return render(request, 'SistemaDeDocumentos/Tutor_CrearReporteSemestralGrupal.html',{
                'gruops': request.user.groups.all(),
                'title': 'Seleccionar Grupos Para Reporte Semestral',
                'tutor': tutor,
                'realizado': 1,
                'exito': 'Reporte enviado con éxito'
            })
            # except:
            #     return render(request, 'SistemaDeDocumentos/Tutor_CrearReporteSemestralGrupal.html',{
            #         'gruops': request.user.groups.all(),
            #         'title': 'Seleccionar Grupos Para Reporte Semestral',
            #         'tutor': tutor,
            #         'realizado': 0,
            #         'form': formularios2,
            #         'error': 'No se ha podido enviar con éxito'
            #     })
        else:
            return render(request, 'SistemaDeDocumentos/Tutor_CrearReporteSemestralGrupal.html',{
                'gruops': request.user.groups.all(),
                'title': 'Seleccionar Grupos Para Reporte Semestral',
                'tutor': tutor,
                'realizado': 0,
                'form': formularios2,
                'error': 'No se ha podido enviar con éxito'
            })





@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def SelectReportesSemestralesGrupalesCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    tutores = PersonalTec.objects.filter(idDepartamentoAcademico_id = coordinador.idDepartamentoAcademico.id)
    grupos = Grupo.objects.filter(idPersonalTec__in = tutores).exclude(idEstado_id = estadoCerrado.id)
    reportesGrupales = ReporteSemestralGrupalV2.objects.filter(grupo__in = grupos, ano = coordinador.idInstitucion.anoActual, periodo = coordinador.idInstitucion.periodoActual)
    return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectGruposReporteSemestral.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Reportes Semestrales Grupales Para Reporte Semestral Departamental',
        'coordinador': coordinador,
        'tutores': tutores,
        'grupos': grupos,
        'reportesGrupales': reportesGrupales
    })

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
@transaction.atomic
def CrearReporteSemestralDepartamentalCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)

    try:
        reporte = ReporteSemestralDepartamentalV2.objects.get(ano = coordinador.idInstitucion.anoActual, periodo = coordinador.idInstitucion.periodoActual, coordinador_id = coordinador.id)
        return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamental.html',{
            'gruops': request.user.groups.all(),
            'title': 'Seleccionar Grupos Para Reporte Semestral',
            'coordinador': coordinador,
            'reporte': reporte,
            'realizado': 1
        })
    except:
        pass

    estadoCerrado = Estado.objects.get(estado = 'Cerrado')
    tutores = PersonalTec.objects.filter(idDepartamentoAcademico_id = coordinador.idDepartamentoAcademico.id)
    grupos = Grupo.objects.filter(idPersonalTec__in = tutores).exclude(idEstado_id = estadoCerrado.id)
    noGrupos = grupos.count()
    formularioPrincipal = FormReporteSemestralDepartamentalV2
    formularios = modelformset_factory(TutorReporteSemestralDepartamentalV2, form = FormTutorReporteSemestralDepartamentalV2, extra = noGrupos)

    if request.method == 'GET':
        formularios2 = formularios()
        for indice, form in enumerate(formularios2):
            ele1 = [(grupos[indice].id, grupos[indice].grupo)]
            ele2 = [(grupos[indice].idPersonalTec.id, grupos[indice].idPersonalTec)]
            form.fields['grupo'].choices = ele1
            form.fields['tutor'].choices = ele2
        return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamental.html',{
            'gruops': request.user.groups.all(),
            'title': 'Seleccionar Grupos Para Reporte Semestral',
            'coordinador': coordinador,
            'realizado': 0,
            'form': formularios2,
            'formPrincipal': formularioPrincipal
        })
    else:
        formularios2 = formularios(request.POST)
        formularioPrincipal = formularioPrincipal(request.POST)

        if formularios2.is_valid() and formularioPrincipal.is_valid():
            try:
                instancias = formularios2.save(commit = False)
                estadoAceptado = Estado.objects.get(estado = 'Aceptado')
                formularioPrinNuevo = formularioPrincipal.save(commit = False)
                formularioPrinNuevo.ano = coordinador.idInstitucion.anoActual
                formularioPrinNuevo.periodo = coordinador.idInstitucion.periodoActual
                formularioPrinNuevo.departamento_id = coordinador.idDepartamentoAcademico.id
                formularioPrinNuevo.coordinador_id = coordinador.id
                formularioPrinNuevo.estado_id = estadoAceptado.id
                formularioPrinNuevo.save()
                print(formularioPrinNuevo.id)

                for item in instancias:
                    item.reporte_id = formularioPrinNuevo.id
                    item.save()

                ahora = datetime.now()

                coordTutoDeptAcade = PersonalTec.objects.filter(idDepartamentoAcademico_id = coordinador.idDepartamentoAcademico.id)
                coordTutoDeptAcade2 = []
                for coor in coordTutoDeptAcade:
                    if pertenece_cualquier_grupo(coor.user, ['Coordinador de Tutoria del Departamento Académico']):
                        coordTutoDeptAcade2.append(coor)
                
                jefeDeptAcade2 = []
                for coor in coordTutoDeptAcade:
                    if pertenece_cualquier_grupo(coor.user, ['Jefe de Departamento Académico']):
                        jefeDeptAcade2.append(coor)

                context = {
                    'departamento': coordinador.idDepartamentoAcademico.departamentoAcademico,
                    'coordinador': coordinador.user.first_name + ' ' + coordinador.user.last_name,
                    'fecha': ahora.strftime("%d/%m/%Y"),
                    'hora': ahora.strftime("%H:%M:%S"),
                    'tutores': instancias,
                    'coordTutoDeptAcade': coordTutoDeptAcade2[0].user,
                    'jefeDeptAcade': jefeDeptAcade2[0].user,
                    'actividad1': formularioPrinNuevo.actividad1,
                    'actividad2': formularioPrinNuevo.actividad2,
                    'actividad3': formularioPrinNuevo.actividad3,
                    'actividad4': formularioPrinNuevo.actividad4,
                    'actividad5': formularioPrinNuevo.actividad5,
                    'actividad6': formularioPrinNuevo.actividad6,
                    'actividad7': formularioPrinNuevo.actividad7,
                    'actividad8': formularioPrinNuevo.actividad8,
                    'actividad9': formularioPrinNuevo.actividad9,
                    'actividad10': formularioPrinNuevo.actividad10,
                    'acciones': formularioPrinNuevo.acciones
                }

                templateReporte = DocxTemplate("Tutoria/static/Templates/Template_ReporteSemestralDepartamentalCoord.docx")
                nombre = coordinador.user.username + "ReporteSemestralDepartamental" + ahora.strftime("__%d_%m_%Y_%H_%M_%S")
                inicioRuta = "Tutoria/static/borrar/"
                inicioRutaReporte = "Tutoria/static/Archivos/Reportes/"
                templateReporte.render(context)
                templateReporte.save(inicioRuta + nombre + ".docx")
                pythoncom.CoInitialize()
                convert(inicioRuta + nombre + ".docx", inicioRutaReporte + nombre + ".pdf")
                formularioPrinNuevo.archivo = "Archivos/Reportes/" + nombre + ".pdf"
                formularioPrinNuevo.save()

                return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamental.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Seleccionar Grupos Para Reporte Semestral',
                    'coordinador': coordinador,
                    'realizado': 1,
                    'exito': 'Reporte enviado con éxito'
                })
            except:
                for indice, form in enumerate(formularios2):
                    ele1 = [(grupos[indice].id, grupos[indice].grupo)]
                    ele2 = [(grupos[indice].idPersonalTec.id, grupos[indice].idPersonalTec)]
                    form.fields['grupo'].choices = ele1
                    form.fields['tutor'].choices = ele2
                return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamental.html',{
                    'gruops': request.user.groups.all(),
                    'title': 'Seleccionar Grupos Para Reporte Semestral',
                    'coordinador': coordinador,
                    'realizado': 0,
                    'form': formularios2,
                    'formPrincipal': formularioPrincipal,
                    'error': 'No se ha podido enviar con éxito'
                })

        else:
            for indice, form in enumerate(formularios2):
                ele1 = [(grupos[indice].id, grupos[indice].grupo)]
                ele2 = [(grupos[indice].idPersonalTec.id, grupos[indice].idPersonalTec)]
                form.fields['grupo'].choices = ele1
                form.fields['tutor'].choices = ele2
            return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamental.html',{
                'gruops': request.user.groups.all(),
                'title': 'Seleccionar Grupos Para Reporte Semestral',
                'coordinador': coordinador,
                'realizado': 0,
                'form': formularios2,
                'formPrincipal': formularioPrincipal,
                'error': 'No se ha podido enviar con éxito'
            })

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def VisualizarReportesSemestralesGrupalesCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    tutores = PersonalTec.objects.filter(idDepartamentoAcademico_id = coordinador.idDepartamentoAcademico.id)
    reportes = ReporteSemestralGrupalV2.objects.filter(tutor__in = tutores)
    return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_VisualizarReportesSemestralesGrupales.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Reportes Semestrales Grupales',
        'coordinador': coordinador,
        'tutores': tutores,
        'reportes': reportes
    })

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def VisualizarReportesSemestralesDepartamentalesCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    reportes = ReporteSemestralDepartamentalV2.objects.filter(coordinador_id = coordinador.id)
    return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_VisualizarReportesSemestralesDepartamentales.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Reportes Semestrales Departamentales',
        'coordinador': coordinador,
        'reportes': reportes
    })

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def SelectDiagnosticoInstitucionalCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    try:
        diagnostico = DiagnosticoInstitucionalV2.objects.get(ano = coordinador.idInstitucion.anoActual, periodo = coordinador.idInstitucion.periodoActual, institucion_id = coordinador.idInstitucion.id)
    except:
        diagnostico = None

    try:
        pat = PATDepartamentalV2.objects.get(ano = coordinador.idInstitucion.anoActual, periodo = coordinador.idInstitucion.periodoActual, departamento_id = coordinador.idDepartamentoAcademico.id)
        return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucional.html', {
            'gruops': request.user.groups.all(),
            'title': 'Plan De Acción Tutorial',
            'coordinador': coordinador,
            'diagnostico': diagnostico,
            'realizado': 1
        })
    except:
        pass

    form = FormPATDepartamentalV2()

    if request.method == 'GET':
        return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucional.html', {
            'gruops': request.user.groups.all(),
            'title': 'Plan De Acción Tutorial',
            'coordinador': coordinador,
            'diagnostico': diagnostico,
            'realizado': 0,
            'form': form
        })
    else:
        form = FormPATDepartamentalV2(request.POST, request.FILES)
        if form.is_valid():
            try:
                patNuevo = form.save(commit = False)
                estadoAceptado = Estado.objects.get(estado = 'Aceptado')
                patNuevo.ano = coordinador.idInstitucion.anoActual
                patNuevo.periodo = coordinador.idInstitucion.periodoActual
                patNuevo.departamento_id = coordinador.idDepartamentoAcademico.id
                patNuevo.coordinador_id = coordinador.id
                patNuevo.estado_id = estadoAceptado.id
                patNuevo.save()
                return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucional.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Plan De Acción Tutorial',
                    'coordinador': coordinador,
                    'diagnostico': diagnostico,
                    'realizado': 1,
                    'exito': 'Se ha enviado con éxito'
                })
            except:
                return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucional.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Plan De Acción Tutorial',
                    'coordinador': coordinador,
                    'diagnostico': diagnostico,
                    'realizado': 0,
                    'error': 'No se ha enviado con éxito',
                    'form': form
                })
        else:
            return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucional.html', {
                'gruops': request.user.groups.all(),
                'title': 'Plan De Acción Tutorial',
                'coordinador': coordinador,
                'diagnostico': diagnostico,
                'realizado': 0,
                'error': 'No se ha enviado con éxito',
                'form': form
            })

# @login_required()
# @group_required('Coordinador de Tutoria del Departamento Académico')
# def SubirPlanDeAccionTutorialCoordinador(request):
#     pass

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def VisualizarPlanDeAccionTutorialCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    reportes = PATDepartamentalV2.objects.filter(coordinador_id = coordinador.id)
    return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_VisualizarPlanesAccionTutorialDepartamentales.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Planes De Acción Tutorial',
        'coordinador': coordinador,
        'reportes': reportes
    })

@login_required()
@group_required('Coordinador de Tutoria del Departamento Académico')
def VisualizarDiagnosticoInstitucionalCoordinador(request):
    coordinador = PersonalTec.objects.get(user_id = request.user.id)
    reportes = DiagnosticoInstitucionalV2.objects.filter(institucion_id = coordinador.idInstitucion.id)
    return render(request, 'SistemaDeDocumentos/CoordinadorTutoriaDepartamentoAcademico_VisualizarDiagnosticosInstitucionales.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Diagnósticos Institucionales',
        'coordinador': coordinador,
        'reportes': reportes
    })





@login_required()
@group_required('Coordinación Institucional de Tutoría')
def CrearDiagonsticoInstitucionalTutoriaCoordinacion(request):
    coordinacion = PersonalTec.objects.get(user_id = request.user.id)

    try:
        diagnostico = DiagnosticoInstitucionalV2.objects.get(ano = coordinacion.idInstitucion.anoActual, periodo = coordinacion.idInstitucion.periodoActual, institucion_id = coordinacion.idInstitucion.id)
        return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoria.html', {
            'gruops': request.user.groups.all(),
            'title': 'Diagnóstico Institucional',
            'coordinacion': coordinacion,
            'diagnostico': diagnostico,
            'realizado': 1
        })
    except:
        pass

    form = FormDiagnosticoInstitucionalV2()

    if request.method == 'GET':
        return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoria.html', {
            'gruops': request.user.groups.all(),
            'title': 'Diagnóstico Institucional',
            'coordinacion': coordinacion,
            'realizado': 0,
            'form': form
        })
    else:
        form = FormDiagnosticoInstitucionalV2(request.POST, request.FILES)
        if form.is_valid():
            try:
                diagNuevo = form.save(commit = False)
                estadoAceptado = Estado.objects.get(estado = 'Aceptado')
                diagNuevo.ano = coordinacion.idInstitucion.anoActual
                diagNuevo.periodo = coordinacion.idInstitucion.periodoActual
                diagNuevo.institucion_id = coordinacion.idInstitucion.id
                diagNuevo.coordinador_id = coordinacion.id
                diagNuevo.estado_id = estadoAceptado.id
                diagNuevo.save()
                return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoria.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Diagnóstico Institucional',
                    'coordinacion': coordinacion,
                    'realizado': 1,
                    'exito': 'Se ha enviado con éxito'
                })
            except:
                return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoria.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Diagnóstico Institucional',
                    'coordinacion': coordinacion,
                    'realizado': 0,
                    'error': 'No se ha enviado con éxito',
                    'form': form
                })
        else:
            return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoria.html', {
                'gruops': request.user.groups.all(),
                'title': 'Diagnóstico Institucional',
                'coordinacion': coordinacion,
                'realizado': 0,
                'error': 'No se ha enviado con éxito',
                'form': form
            })

@login_required()
@group_required('Coordinación Institucional de Tutoría', 'Subdirector Académico')
def VisualizarTodosLosDocumentosCoordinacion(request):
    personal = PersonalTec.objects.get(user_id = request.user.id)
    tutores = PersonalTec.objects.filter(idInstitucion_id = personal.idInstitucion.id)

    reportesGrupales = ReporteSemestralGrupalV2.objects.filter(tutor__in = tutores).order_by('-id')
    reportesDepartamentales = ReporteSemestralDepartamentalV2.objects.filter(coordinador__in = tutores).order_by('-id')
    reportesInstitucionales = ReporteSemestralInstitucionalV2.objects.filter(institucion_id = personal.idInstitucion.id).order_by('-id')
    reportesPATs = PATDepartamentalV2.objects.filter(coordinador__in = tutores).order_by('-id')
    reportesPITs = PITInstitucionalV2.objects.filter(institucion_id = personal.idInstitucion.id).order_by('-id')
    reportesDiagnosticos = DiagnosticoInstitucionalV2.objects.filter(institucion_id = personal.idInstitucion.id).order_by('-id')

    return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_SubdirectorAcademico_VisualizarTodosLosDocumentos.html', {
        'gruops': request.user.groups.all(),
        'title': 'Todos Los Documentos',
        'reportesGrupales': reportesGrupales,
        'reportesDepartamentales': reportesDepartamentales,
        'reportesInstitucionales': reportesInstitucionales,
        'reportesPATs': reportesPATs,
        'reportesPITs': reportesPITs,
        'reportesDiagnosticos': reportesDiagnosticos
    })


@login_required()
@group_required('Coordinación Institucional de Tutoría')
@transaction.atomic
def IntegrarReporteSemestralInstitucionalCoordinacion(request):
    coordinacion = PersonalTec.objects.get(user_id = request.user.id)
    try:
        reporte = ReporteSemestralInstitucionalV2.objects.get(ano = coordinacion.idInstitucion.anoActual, periodo = coordinacion.idInstitucion.periodoActual, coordinador_id = coordinacion.id)
        realizado = 1
    except:
        realizado = 0

    departamentos = DepartamentoAcademico.objects.filter(idInstitucion_id = coordinacion.idInstitucion.id)
    personal = PersonalTec.objects.filter(idInstitucion_id = coordinacion.idInstitucion.id)
    personal2 = []
    for coor in personal:
        if pertenece_cualquier_grupo(coor.user, ['Coordinador de Tutoria del Departamento Académico']):
            personal2.append(coor)
    reportesDepartamentales = ReporteSemestralDepartamentalV2.objects.filter(ano = coordinacion.idInstitucion.anoActual, periodo = coordinacion.idInstitucion.periodoActual, coordinador__in = personal2)
    form = FormConfirmacionReporteInstitucional()

    if request.method == 'GET':
        return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_IntegrarReporteSemestralInstitucional.html', {
            'gruops': request.user.groups.all(),
            'title': 'Integrar Reporte Semestral Institucional',
            'realizado': realizado,
            'departamentos': departamentos,
            'reportesDepartamentales': reportesDepartamentales,
            'form': form,
            'coordinadores': personal2
        })
    else:
        form = FormConfirmacionReporteInstitucional(request.POST)
        if form.is_valid():
            try:
                if realizado == 1:
                    reporte.delete()
                merger = PdfFileMerger()
                #Create a list with file names
                pdf_files = []
                for rep in reportesDepartamentales:
                    pdf_files.append("Tutoria/static/" + rep.archivo)
                #Iterate over the list of file names
                for pdf_file in pdf_files:
                    #Append PDF files
                    merger.append(pdf_file)
                #Write out the merged PDF
                ahora = datetime.now()
                nombre = coordinacion.user.username + "ReporteSemestralInstitucional" + ahora.strftime("__%d_%m_%Y_%H_%M_%S") + ".pdf"
                merger.write("Tutoria/static/Archivos/Reportes/" + nombre)
                merger.close()

                reporteNuevo = ReporteSemestralInstitucionalV2()
                estadoAceptado = Estado.objects.get(estado = 'Aceptado')
                reporteNuevo.archivo = "Archivos/Reportes/" + nombre
                reporteNuevo.ano = coordinacion.idInstitucion.anoActual
                reporteNuevo.periodo = coordinacion.idInstitucion.periodoActual
                reporteNuevo.institucion_id = coordinacion.idInstitucion.id
                reporteNuevo.coordinador_id = coordinacion.id
                reporteNuevo.estado_id = estadoAceptado.id
                reporteNuevo.save()
                return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_IntegrarReporteSemestralInstitucional.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Integrar Reporte Semestral Institucional',
                    'realizado': 1,
                    'departamentos': departamentos,
                    'reportesDepartamentales': reportesDepartamentales,
                    'form': form,
                    'exito': 'Se ha integrado con éxito el reporte',
                    'coordinadores': personal2
                })
            except:
                return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_IntegrarReporteSemestralInstitucional.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Integrar Reporte Semestral Institucional',
                    'realizado': realizado,
                    'departamentos': departamentos,
                    'reportesDepartamentales': reportesDepartamentales,
                    'form': form,
                    'error': 'Ha ocurrido un error al integrar el reporte',
                    'coordinadores': personal2
                })

        else:
            return render(request, 'SistemaDeDocumentos/CoordinacionInstitucionalTutoria_IntegrarReporteSemestralInstitucional.html', {
                'gruops': request.user.groups.all(),
                'title': 'Integrar Reporte Semestral Institucional',
                'realizado': realizado,
                'departamentos': departamentos,
                'reportesDepartamentales': reportesDepartamentales,
                'form': form,
                'error': 'Ha ocurrido un error al integrar el reporte',
                'coordinadores': personal2
            })





@login_required()
@group_required('Jefe de Desarrollo Académico')
@transaction.atomic
def IntegrarProgramaInstitucionalTutorialJefe(request):
    jefe = PersonalTec.objects.get(user_id = request.user.id)
    try:
        reporte = PITInstitucionalV2.objects.get(ano = jefe.idInstitucion.anoActual, periodo = jefe.idInstitucion.periodoActual, jefe_id = jefe.id)
        realizado = 1
    except:
        realizado = 0

    departamentos = DepartamentoAcademico.objects.filter(idInstitucion_id = jefe.idInstitucion.id)
    personal = PersonalTec.objects.filter(idInstitucion_id = jefe.idInstitucion.id)
    personal2 = []
    for coor in personal:
        if pertenece_cualquier_grupo(coor.user, ['Coordinador de Tutoria del Departamento Académico']):
            personal2.append(coor)
    patDepartamentales = PATDepartamentalV2.objects.filter(ano = jefe.idInstitucion.anoActual, periodo = jefe.idInstitucion.periodoActual, coordinador__in = personal2)
    form = FormConfirmacionReporteInstitucional()

    if request.method == 'GET':
        return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_IntegrarProgramaInsitucionalTutorial.html', {
            'gruops': request.user.groups.all(),
            'title': 'Integrar Programa Institucional Tutorial',
            'realizado': realizado,
            'departamentos': departamentos,
            'patDepartamentales': patDepartamentales,
            'form': form,
            'coordinadores': personal2
        })
    else:
        form = FormConfirmacionReporteInstitucional(request.POST)
        if form.is_valid():
            try:
                if realizado == 1:
                    reporte.delete()
                merger = PdfFileMerger()
                #Create a list with file names
                pdf_files = []
                for rep in patDepartamentales:
                    pdf_files.append( rep.archivo.url.replace("/media/", "media/"))
                #Iterate over the list of file names
                for pdf_file in pdf_files:
                    #Append PDF files
                    merger.append(pdf_file)
                #Write out the merged PDF
                ahora = datetime.now()
                nombre = jefe.user.username + "ProgramaInstitucionalTutorial" + ahora.strftime("__%d_%m_%Y_%H_%M_%S") + ".pdf"
                merger.write("Tutoria/static/Archivos/Reportes/" + nombre)
                merger.close()

                reporteNuevo = PITInstitucionalV2()
                estadoAceptado = Estado.objects.get(estado = 'Aceptado')
                reporteNuevo.archivo = "Archivos/Reportes/" + nombre
                reporteNuevo.ano = jefe.idInstitucion.anoActual
                reporteNuevo.periodo = jefe.idInstitucion.periodoActual
                reporteNuevo.institucion_id = jefe.idInstitucion.id
                reporteNuevo.jefe_id = jefe.id
                reporteNuevo.estado_id = estadoAceptado.id
                reporteNuevo.save()
                return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_IntegrarProgramaInsitucionalTutorial.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Integrar Programa Institucional Tutorial',
                    'realizado': 1,
                    'departamentos': departamentos,
                    'patDepartamentales': patDepartamentales,
                    'form': form,
                    'exito': 'Se ha integrado con éxito el reporte',
                    'coordinadores': personal2
                })
            except:
                return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_IntegrarProgramaInsitucionalTutorial.html', {
                    'gruops': request.user.groups.all(),
                    'title': 'Integrar Programa Institucional Tutorial',
                    'realizado': realizado,
                    'departamentos': departamentos,
                    'patDepartamentales': patDepartamentales,
                    'form': form,
                    'error': 'Ha ocurrido un error al integrar el reporte',
                    'coordinadores': personal2
                })

        else:
            return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_IntegrarProgramaInsitucionalTutorial.html', {
                'gruops': request.user.groups.all(),
                'title': 'Integrar Programa Institucional Tutorial',
                'realizado': realizado,
                'departamentos': departamentos,
                'patDepartamentales': patDepartamentales,
                'form': form,
                'error': 'Ha ocurrido un error al integrar el reporte',
                'coordinadores': personal2
            })

@login_required()
@group_required('Jefe de Desarrollo Académico')
def VisualizarProgramaInstitucionalTutorialJefe(request):
    jefe = PersonalTec.objects.get(user_id = request.user.id)
    programas = PITInstitucionalV2.objects.filter(institucion_id = jefe.idInstitucion.id)
    return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_VisualizarProgramasInsitucionalesTutorial.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Programas Institucionales Tutoriales',
        'programas': programas
    })


@login_required()
@group_required('Jefe de Desarrollo Académico')
def VisualizarPlanAccionTutorialJefe(request):
    jefe = PersonalTec.objects.get(user_id = request.user.id)
    departamentos = DepartamentoAcademico.objects.filter(idInstitucion_id = jefe.idInstitucion.id)
    patsDepartamentales = PATDepartamentalV2.objects.filter(departamento__in = departamentos).order_by('-id')
    return render(request, 'SistemaDeDocumentos/JefeDesarrolloAcademico_VisualizarPlanesAccionTutorial.html', {
        'gruops': request.user.groups.all(),
        'title': 'Visualizar Planes de Acción Tutorial',
        'patsDepartamentales': patsDepartamentales
    })