from django.urls import path
from . import views

urlpatterns = [
    #url de inicio, login y logout
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('LogOut', views.cierreSesion, name='cierreSesion'),
    path('Inicio', views.paginaInicio, name='paginaInicio'),

    #urls de tutorado
    path('Tutorado/Cuestionarios/', views.cuestionariosTutorado, name='cuestionariosTutorado'),
    path('Tutorado/Cuestionarios/Enviar/<int:cuestionario_id>', views.enviarCuestionarioTutorado, name='enviarCuestionarioTutorado'),
    path('Tutorado/Perfil', views.perfilTutorado, name = 'perfilTutorado'),
    path('Tutorado/Citas/<int:page>', views.misCitasTutorado, name = 'misCitasTutorado'),
    path('Tutorado/CambioPassword', views.cambiarPassword, name = 'cambiarPassword'),
    path('Tutorado/EditarInformacion', views.editarInformacion, name = 'editarInformacion'),

    #urls para todos menos el tutorado
    path('Documentacion/', views.Documentacion, name = 'documentos'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('Grupos/', views.gruposTutor, name = 'gruposTutor'),
    path('Grupos/<int:grupo_id>', views.grupoTutor, name = 'grupoTutor'),
    path('Grupos/<int:grupo_id>/Ayuda/Psicologica/<int:tutorado_id>', views.solicitudPsicologigaTutor, name = 'solicitarAyudaPsicologicaTutor'),
    path('Cuestionario/Crear', views.crearCuestionario, name = 'crearCuestionario'),
    path('Cuestionario/Resultados', views.resultadosCuestionarios, name = 'verResultadosCuestionarios'),
    path('Cuestionario/Resultados/<int:grupo_id>', views.verResultadosCuestionariosGrupo, name = 'verResultadosCuestionariosGrupo'),
    path('Tutor/CambioPassword', views.cambiarPasswordTutor, name = 'cambiarPasswordTutor'),

    path('CoordinadorDepartamental/listaTutor', views.listaTutor, name = 'listaTutor'),
    path('CoordinadorDepartamental/crearGrupo/<int:Tutor>', views.crearGrupo, name = 'crearGrupo'),
    path('CoordinadorDepartamental/verGruposDelTutor/<int:Tutor>', views.verGruposDelTutor, name = 'verGruposDelTutor'),
    path('CoordinadorDepartamental/listarAlumnos/<int:Grupoid>', views.listarAlumnos, name = 'listarAlumnos'),
    
    #pruebas
    path('prueba/', views.prueba, name = 'Prueba'),
    
]