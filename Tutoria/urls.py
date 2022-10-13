from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioSesion, name = 'inicioSesion'),
    path('Documentacion/', views.Documentacion, name = 'Documentacion'),
    path('verDocumentacion/', views.verDocumentacion, name = 'verDocumentacion'),
    path('crearDocumento/', views.crearDocumento, name = 'crearDocumento'),
    path('perfilTodos/', views.perfilTodos, name = 'perfilTodos'),
    path('1/', views.a1, name = 'a1'),
    path('2/', views.a2, name = 'a2'),
    path('3/', views.a3, name = 'a3'),
    path('4/', views.a4, name = 'a4'),
    path('5/', views.a5, name = 'a5'),
    path('6/', views.a6, name = 'a6'),
    path('7/', views.a7, name = 'a7'),
    path('8/', views.a8, name = 'a8'),
    path('9/', views.a9, name = 'a9'),
    path('10/', views.a10, name = 'a10'),
    path('11/', views.a11, name = 'a11'),
    path('12/', views.a12, name = 'a12'),
    path('13/', views.a13, name = 'a13')
]