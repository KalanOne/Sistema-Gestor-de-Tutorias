from django.urls import path
from . import views, documentosViews

urlpatterns = [
    #url de inicio, login y logout
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('LogOut', views.cierreSesion, name='cierreSesion'),
    path('Inicio', views.paginaInicio, name='paginaInicio'),

    #urls de tutorado
    path('Tutorado/Cuestionarios/', views.cuestionariosTutorado, name='cuestionariosTutorado'),
    path('Tutorado/Cuestionarios/Enviar/<int:cuestionario_id>', views.enviarCuestionarioTutorado, name='enviarCuestionarioTutorado'),
    path('Tutorado/Perfil', views.perfilTutorado, name = 'perfilTutorado'),
    # path('Tutorado/Citas/<int:page>', views.misCitasTutorado, name = 'misCitasTutorado'),
    path('Tutorado/Citas', views.misCitasTutorado, name = 'misCitasTutorado'),
    path('Tutorado/EditarInformacion', views.editarInformacion, name = 'editarInformacion'),

    #urls para todos menos el tutorado
    path('Documentacion/', views.Documentacion, name = 'documentos'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    # path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('ReporteSemestral', views.reporteSemestralGrupal, name='reporteSemestral'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('Grupos/', views.gruposTutor, name = 'gruposTutor'),
    path('Grupos/<int:grupo_id>', views.grupoTutor, name = 'grupoTutor'),
    path('Grupos/<int:grupo_id>/Ayuda/Psicologica/<int:tutorado_id>', views.solicitudPsicologigaTutor, name = 'solicitarAyudaPsicologicaTutor'),
    path('Cuestionario/Crear', views.crearCuestionario, name = 'crearCuestionario'),
    path('Cuestionario/Resultados', views.resultadosCuestionarios, name = 'verResultadosCuestionarios'),
    path('Cuestionario/Resultados/<int:grupo_id>', views.verResultadosCuestionariosGrupo, name = 'verResultadosCuestionariosGrupo'),

    # urls para Jefe de Departamento Académico
    path('JefeDepartamentoAcademico/listaTutor', views.listaTutor, name = 'listaTutor'),
    path('JefeDepartamentoAcademico/crearGrupo/<int:Tutor>', views.crearGrupo, name = 'crearGrupo'),
    path('JefeDepartamentoAcademico/verGruposDelTutor/<int:Tutor>', views.verGruposDelTutor, name = 'verGruposDelTutor'),
    path('JefeDepartamentoAcademico/listarAlumnos/<int:Grupoid>', views.listarAlumnos, name = 'listarAlumnos'),

    # urls para Coordinador de Tutoria del Departamento Académico
    path('CoordinadorDepartamental/ReportesSemestralesGrupales', views.verReportesSemestralesGrupales, name = 'verReportesSemestralesGrupales'),
    path('CoordinadorDepartamental/ReporteSemestral', views.reporteSemestralDept, name = 'reporteSemestralDpt'),
    path('CoordinadorDepartamental/PAT', views.reportePAT, name = 'reportePAT'),

    # urls Coordinación Institucional de Tutoría
    path('CoordinadorInstitucional/ReporteSemestralInstitucional', views.reporteSemestralInst, name = 'reporteSemestralInst'),
    path('CoordinadorInstitucional/ReportesSemestralesDpt', views.verReportesSemestralesDpt, name = 'verReportesSemestralesDpt'),

    path('Cambiar/Contraseña', views.cambiarContraseña, name='cambiarContraseña'),
    path('Todos/EditarInformacion', views.editarInformacionTodos, name='editarInformacionTodos'),

    #pruebas
    path('registrarTutorados//<int:Grupoid>', views.registrarTutorados, name = 'registrarTutorados'),
    

    # urls Para documentos
    path('Tutor/V2/ReporteSemestral/Grupos/', documentosViews.SelectGruposReporteSemestral, name = 'Tutor_SelectGruposReporteSemestralV2'),
    path('Tutor/V2/ReporteSemestral/Grupal/Visualizar/', documentosViews.VisualizarReportesSemestralesGrupalesTutor, name = 'Tutor_VerReportesSemestralesV2'),
    path('Tutor/V2/ReporteSemestral/Grupos/<int:grupo_id>/', documentosViews.CrearReporteSemestralGrupal, name = 'Tutor_CrearReporteSemestralV2'),



    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamento/', documentosViews.SelectReportesSemestralesGrupalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_SelectReporteSemestralGrupalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamento/Crear/', documentosViews.CrearReporteSemestralDepartamentalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_CrearReporteSemestralDepartamentalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Grupal/Visualizar/', documentosViews.VisualizarReportesSemestralesGrupalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarReporteSemestralGrupalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/ReporteSemestral/Departamental/Visualizar/', documentosViews.VisualizarReportesSemestralesDepartamentalesCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarReporteSemestralDepartamentalV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/PlanDeAccionTutorial/Departamental/', documentosViews.SelectDiagnosticoInstitucionalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_SelectDiagnosticoInstitucionalV2'),
    # path('CoordinadorTutoriaDepartamentoAcademico/V2/PlanDeAccionTutorial/Departamental/Crear/', documentosViews.SubirPlanDeAccionTutorialCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_SubirPlanDeAccionTutorialV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/PlanDeAccionTutorial/Departamental/Visualizar/', documentosViews.VisualizarPlanDeAccionTutorialCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarPlanDeAccionTutorialV2'),
    path('CoordinadorTutoriaDepartamentoAcademico/V2/DiagnosticoInstitucional/Visualizar/', documentosViews.VisualizarDiagnosticoInstitucionalCoordinador, name = 'CoordinadorTutoriaDepartamentoAcademico_VisualizarDiagnosticoInstitucionalV2'),
    


    path('CoordinacionInstitucionalTutoria/V2/DiagnosticoInstitucional/Crear/', documentosViews.CrearDiagonsticoInstitucionalTutoriaCoordinacion, name = 'CoordinacionInstitucionalTutoria_CrearDiagnosticoInstitucionalTutoriaV2'),
    path('CoordinacionInstitucionalTutoria/V2/Documentos/Visualizar/', documentosViews.VisualizarTodosLosDocumentosCoordinacion, name = 'CoordinacionInstitucionalTutoria_VisualizarTodosLosDocumentosV2'),
    path('CoordinacionInstitucionalTutoria/V2/ReporteSemestralInstitucional/Integrar/', documentosViews.IntegrarReporteSemestralInstitucionalCoordinacion, name = 'CoordinacionInstitucionalTutoria_IntregarReporteInstitucionalTutoriaV2'),



    path('JefeDesarrolloAcademico/V2/ProgramaInstitucional/Integrar/', documentosViews.IntegrarProgramaInstitucionalTutorialJefe, name = 'JefeDesarrolloAcademico_IntregarProgramaInstitucionalTutorialV2'),
    path('JefeDesarrolloAcademico/V2/ProgramaInstitucional/Visualizar/', documentosViews.VisualizarProgramaInstitucionalTutorialJefe, name = 'JefeDesarrolloAcademico_VisualizarProgramaInstitucionalTutorialV2'),
    path('JefeDesarrolloAcademico/V2/PlanAccionTutorial/Visualizar/', documentosViews.VisualizarPlanAccionTutorialJefe, name = 'JefeDesarrolloAcademico_VisualizarPlanAccionTutorialV2'),


    # Psicologo y medico
    path('Psicologo/Citas/', documentosViews.CitasPsicologo, name = 'Psicologo_VisualizarCitas'),
    path('Psicologo/Citas/Asignar/<int:cita_id>/', documentosViews.AsignarCita, name = 'Psicologo_AsignarCita'),
    path('Psicologo/Citas/Concluir/<int:cita_id>/', documentosViews.ConcluirCita, name = 'Psicologo_ConcluirCita'),


    #fer
    path('credito/subir/', views.subir_credito, name = 'subir_credito'),
    path('credito/ver/', views.ver_credito_tutorado, name = 'ver_credito_tutorado'),
    path('credito/tutor/', views.ver_credito_tutor, name = 'ver_credito_tutor'),
    path('credito/editar/<int:dato>', views.editar_credito, name = 'editar_credito'),
    path('credito/revisar/<int:dato>', views.revisar_credito, name = 'revisar_credito'),

]