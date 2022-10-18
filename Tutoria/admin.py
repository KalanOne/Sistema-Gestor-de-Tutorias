from django.contrib import admin
from .models import Cuestionario, Tutorado, Grupo, DepartamentoAcademico, Institucion, PersonalTec

# Register your models here.

admin.site.register(Cuestionario)
admin.site.register(Tutorado)
admin.site.register(Grupo)
admin.site.register(DepartamentoAcademico)
admin.site.register(Institucion)
admin.site.register(PersonalTec)