from django.urls import path
from . import views

urlpatterns = [
    #url de inicio, login y logout
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('LogOut', views.cierreSesion, name='cierreSesion'),
    path('Inicio', views.paginaInicio, name='paginaInicio'),

    #urls de tutorado
    path('Tutorado/Cuestionarios/', views.cuestionariosTutorado, name='cuestionariosTutorado'),
    path('Tutorado/Cuestionarios/Realizar/<int:cuestionario_id>', views.cuestionariosTutorado, name='realizarCuestionarioTutorado'),
    path('perfilTutorado/', views.perfilTutorado, name = 'perfilTutorado'),
    path('miscitas/', views.miscitas, name = 'miscitas'),

    #urls para todos menos el tutorado
    path('Documentacion/', views.Documentacion, name = 'documentos'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('gruposTutor/', views.gruposTutor, name = 'gruposTutor'),
    path('crearCuestionario/', views.crearCuestionario, name = 'crearCuestionario'),
    
    #pruebas
    path('prueba/', views.prueba, name = 'Prueba'),
    path('excel2/', views.Excel2, name = 'Excel2'),
    path('credito/subir/', views.subir_credito, name = 'subir_credito'),
    path('credito/ver/', views.ver_credito_tutorado, name = 'ver_credito_tutorado'),
    path('credito/tutor/', views.ver_credito_tutor, name = 'ver_credito_tutor'),
    path('credito/editar/', views.editar_credito, name = 'editar_credito'),
    
]