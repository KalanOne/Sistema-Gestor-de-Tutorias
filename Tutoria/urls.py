from django.urls import path
from . import views, documentosViews

urlpatterns = [
    #url de inicio, login y logout
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('LogOut/', views.cierreSesion, name='cierreSesion'),
    path('Inicio/', views.paginaInicio, name='paginaInicio'),

    #urls de tutorado
    path('Tutorado/Cuestionarios/', views.cuestionariosTutorado, name='cuestionariosTutorado'),
    path('Tutorado/Cuestionarios/Enviar/<int:cuestionario_id>/', views.enviarCuestionarioTutorado, name='enviarCuestionarioTutorado'),
    path('Tutorado/Perfil/', views.perfilTutorado, name = 'perfilTutorado'),
    path('Tutorado/Citas/', views.misCitasTutorado, name = 'misCitasTutorado'),
    path('Tutorado/EditarInformacion/', views.editarInformacion, name = 'editarInformacion'),

    #urls para todos menos el tutorado
    path('Perfil/Todos/', views.perfilTodos, name = 'perfilTodos'),
    path('Grupos/', views.gruposTutor, name = 'gruposTutor'),
    path('Grupos/<int:grupo_id>/', views.grupoTutor, name = 'grupoTutor'),
    path('Grupos/<int:grupo_id>/Ayuda/Psicologica/<int:tutorado_id>/', views.solicitudPsicologigaTutor, name = 'solicitarAyudaPsicologicaTutor'),
    path('Cuestionario/Crear/', views.crearCuestionario, name = 'crearCuestionario'),
    path('Cuestionario/Resultados/', views.resultadosCuestionarios, name = 'verResultadosCuestionarios'),
    path('Cuestionario/Resultados/<int:grupo_id>/', views.verResultadosCuestionariosGrupo, name = 'verResultadosCuestionariosGrupo'),

    # urls para Jefe de Departamento Académico
    path('JefeDepartamentoAcademico/listaTutor/', views.listaTutor, name = 'listaTutor'),
    path('JefeDepartamentoAcademico/crearGrupo/<int:Tutor>/', views.crearGrupo, name = 'crearGrupo'),
    path('JefeDepartamentoAcademico/verGruposDelTutor/<int:Tutor>/', views.verGruposDelTutor, name = 'verGruposDelTutor'),
    path('JefeDepartamentoAcademico/listarAlumnos/<int:Grupoid>/', views.listarAlumnos, name = 'listarAlumnos'),

    path('Cambiar/Contrasena/', views.cambiarContraseña, name='cambiarContraseña'),
    path('Todos/EditarInformacion/', views.editarInformacionTodos, name='editarInformacionTodos'),


    #pruebas
    #path('Registrar/Tutorados/<int:Grupoid>/', views.registrarTutorados, name = 'registrarTutorados'),
    path('listadoPersonal/', views.listado_Personal, name='listadoPersonal'),
    

    # urls Para documentos
    path('Tutor/V2/ReporteSemestral/Grupos/', documentosViews.SelectGruposReporteSemestral, name = 'Tutor_SelectGruposReporteSemestralV2'),
    path('Tutor/V2/ReporteSemestral/Grupal/Visualizar/', documentosViews.VisualizarReportesSemestralesGrupalesTutor, name = 'Tutor_VerReportesSemestralesV2'),
    path('Tutor/V2/ReporteSemestral/Grupos/<int:grupo_id>/', documentosViews.CrearReporteSemestralGrupal, name = 'Tutor_CrearReporteSemestralV2'),



    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamento/', documentosViews.SelectReportesSemestralesGrupalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_SelectReporteSemestralGrupalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamento/Crear/', documentosViews.CrearReporteSemestralDepartamentalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamentalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Grupal/Visualizar/', documentosViews.VisualizarReportesSemestralesGrupalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarReporteSemestralGrupalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamental/Visualizar/', documentosViews.VisualizarReportesSemestralesDepartamentalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarReporteSemestralDepartamentalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/PlanDeAccionTutorial/Departamental/', documentosViews.SelectDiagnosticoInstitucionalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucionalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/PlanDeAccionTutorial/Departamental/Visualizar/', documentosViews.VisualizarPlanDeAccionTutorialCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarPlanDeAccionTutorialV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/DiagnosticoInstitucional/Visualizar/', documentosViews.VisualizarDiagnosticoInstitucionalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarDiagnosticoInstitucionalV2'),
    


    path('CoordinacionInstitucionalTutoria/V2/DiagnosticoInstitucional/Crear/', documentosViews.CrearDiagonsticoInstitucionalTutoriaCoordinacion, name = 'CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoriaV2'),
    path('CoordinacionInstitucionalTutoria/V2/Documentos/Visualizar/', documentosViews.VisualizarTodosLosDocumentosCoordinacion, name = 'CoordinacionInstitucionalTutoria_VisualizarTodosLosDocumentosV2'),
    path('CoordinacionInstitucionalTutoria/V2/ReporteSemestralInstitucional/Integrar/', documentosViews.IntegrarReporteSemestralInstitucionalCoordinacion, name = 'CoordinacionInstitucionalTutoria_IntregarReporteInstitucionalTutoriaV2'),
    path('CoordinacionInstitucionalTutoria/Registrar/CoordinadorTutoriaDepartamentoAcademico/', views.registrarCoordinadorTutoria, name = 'registrarCoordinadorTutoria'),



    path('JefeDesarrolloAcademico/V2/ProgramaInstitucional/Integrar/', documentosViews.IntegrarProgramaInstitucionalTutorialJefe, name = 'JefeDesarrolloAcademico_IntregarProgramaInstitucionalTutorialV2'),
    path('JefeDesarrolloAcademico/V2/ProgramaInstitucional/Visualizar/', documentosViews.VisualizarProgramaInstitucionalTutorialJefe, name = 'JefeDesarrolloAcademico_VisualizarProgramaInstitucionalTutorialV2'),
    path('JefeDesarrolloAcademico/V2/PlanAccionTutorial/Visualizar/', documentosViews.VisualizarPlanAccionTutorialJefe, name = 'JefeDesarrolloAcademico_VisualizarPlanAccionTutorialV2'),
     path('JefeDesarrolloAcademico/Registrar/JefeDepartamentoAcademico/', views.registrarJefeDepartamentoAcademico, name = 'registrarJefeDepartamentoAcademico'),


    # Psicologo y medico
    path('Psicologo/Citas/', documentosViews.CitasPsicologo, name = 'Psicologo_VisualizarCitas'),
    path('Psicologo/Citas/Asignar/<int:cita_id>/', documentosViews.AsignarCita, name = 'Psicologo_AsignarCita'),
    path('Psicologo/Citas/Concluir/<int:cita_id>/', documentosViews.ConcluirCita, name = 'Psicologo_ConcluirCita'),
    path('Medico/Citas/', documentosViews.CitasMedico, name = 'Medico_AsignarCita'),


    # Subdirector
    path('SubdirectorAcademico/Cambio/Periodo/', documentosViews.VisualizarFechasLimites, name = 'Subdirector_CambioPeriodo'),
    path('SubdirectorAcademico/Cambio/DiagnosticoInstitucional/', documentosViews.ModFechaLimiteDiag, name = 'Subdirector_ModFechaLimiteDiag'),
    path('SubdirectorAcademico/Cambio/PlanAccionTutorial/', documentosViews.ModFechaLimitePAT, name = 'Subdirector_ModFechaLimitePAT'),
    path('SubdirectorAcademico/Cambio/ProgramaInstitucionalTutorial/', documentosViews.ModFechaLimitePIT, name = 'Subdirector_ModFechaLimitePIT'),
    path('SubdirectorAcademico/Cambio/ReporteSemestralGrupal/', documentosViews.ModFechaLimiteGrupal, name = 'Subdirector_ModFechaLimiteGrupal'),
    path('SubdirectorAcademico/Cambio/ReporteSemestralDepartamental/', documentosViews.ModFechaLimiteDepartamental, name = 'Subdirector_ModFechaLimiteDepartamental'),
    path('SubdirectorAcademico/Cambio/ReporteSemestralInstitucional/', documentosViews.ModFechaLimiteInstitucional, name = 'Subdirector_ModFechaLimiteInstitucional'),
    path('SubdirectorAcademico/Registrar/JefeDesarrolloAcademico/', views.registrarJefeDesarrolloAca, name = 'registrarJefeDesarrolloAca'),
    path('SubdirectorAcademico/Registrar/CoordinacionInstitucionalTutoria/', views.registrarCoordinacionInstitucional, name = 'registrarCoordinacionInstitucional'),


    #fer
    path('Credito/subir/', views.subir_credito, name = 'subir_credito'),
    path('Credito/ver/', views.ver_credito_tutorado, name = 'ver_credito_tutorado'),
    path('Credito/tutor/', views.ver_credito_tutor, name = 'ver_credito_tutor'),
    path('Credito/editar/<int:dato>/', views.editar_credito, name = 'editar_credito'),
    path('Credito/revisar/<int:dato>/', views.revisar_credito, name = 'revisar_credito'),

]