from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Estado)
admin.site.register(Institucion)
admin.site.register(Grupo)
admin.site.register(DepartamentoAcademico)
admin.site.register(PadreMadreTutor)
admin.site.register(Tutorado)
admin.site.register(PersonalTec)
admin.site.register(PersonalMed)
admin.site.register(Cuestionario)
admin.site.register(GrupoRespuesta)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(RespuestaContestada)
admin.site.register(PIT)
admin.site.register(PAT)
admin.site.register(ReporteSemestralGrupal)
admin.site.register(ReporteSemestralDepartamento)
admin.site.register(ReporteSemestralInstitucional)
admin.site.register(ConstanciaTutor)
admin.site.register(Orden)
admin.site.register(Motivo)
admin.site.register(Cita)

admin.site.register(Excel2)
admin.site.register(Credito)