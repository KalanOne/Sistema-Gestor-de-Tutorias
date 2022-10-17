from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('Inicio', views.paginaInicio, name='paginaInicio'),

    path('Documentacion/', views.Documentacion, name = 'Documentacion'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('pruebas/', views.pruebas, name = 'Prueba'),
]