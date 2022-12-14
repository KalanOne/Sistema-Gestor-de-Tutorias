from django.contrib import admin
from .models import *
from .documentosModels import *

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
admin.site.register(Orden)
admin.site.register(Motivo)
admin.site.register(Cita)
admin.site.register(CuestionarioContestado)
admin.site.register(registrarAlumno)
admin.site.register(Credito)
admin.site.register(registrarPersonalTec)


admin.site.register(ReporteSemestralGrupalV2)
admin.site.register(TutoradoReporteSemestralGrupalV2)
admin.site.register(ReporteSemestralDepartamentalV2)
admin.site.register(TutorReporteSemestralDepartamentalV2)
admin.site.register(ReporteSemestralInstitucionalV2)
admin.site.register(PATDepartamentalV2)
admin.site.register(PITInstitucionalV2)
admin.site.register(DiagnosticoInstitucionalV2)
admin.site.register(ConstanciaTutorV2)
admin.site.register(FechaLimite)