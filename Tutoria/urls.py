from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('LogOut', views.cierreSesion, name='cierreSesion'),
    path('Inicio', views.paginaInicio, name='paginaInicio'),
    path('Tutorado/Cuestionarios/', views.cuestionariosTutorado, name='cuestionariosTutorado'),
    path('Tutorado/Cuestionarios/Realizar/<int:cuestionario_id>', views.cuestionariosTutorado, name='realizarCuestionarioTutorado'),

    path('Documentacion/', views.Documentacion, name = 'documentos'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('perfilTutorado/', views.perfilTutorado, name = 'perfilTutorado'),
    path('prueba/', views.prueba, name = 'Prueba'),
    path('miscitas/', views.miscitas, name = 'miscitas'),
]