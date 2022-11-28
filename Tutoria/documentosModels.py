from django.db import models
from django.utils.timezone import now
from .models import *

class ReporteSemestralGrupalV2(models.Model):
    archivo = models.CharField(max_length = 200, null = True, blank = True)
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)
    tutor = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.archivo, self.ano, self.periodo, self.fecha, self.grupo)

    class Meta:
        verbose_name= 'ReporteSemestralGrupalV2'
        verbose_name_plural= 'ReportesSemestralesGrupalesV2'
        db_table= 'reporteSemestralGrupalV2'
        ordering= ['id']

class TutoradoReporteSemestralGrupalV2(models.Model):
    desempeno = [
        ('Excelente', 'Excelente'),
        ('Notable', 'Notable'),
        ('Bueno', 'Bueno'),
        ('Suficiente', 'Suficiente'),
        ('Insuficiente', 'Insuficiente')
    ]
    tutorado = models.ForeignKey('Tutorado', on_delete = models.CASCADE)
    tutoriaGrupal = models.CharField(max_length = 200)
    tutoriaIndividual = models.CharField(max_length = 200)
    observaciones = models.CharField(max_length = 20,choices = desempeno)
    estudianteCanalizado = models.TextField()
    asistencia = models.FloatField()
    credito = models.BooleanField(null = True)
    reporte = models.ForeignKey('ReporteSemestralGrupalV2', on_delete = models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.tutoriaGrupal, self.tutoriaIndividual, self.observaciones, self.asistencia)

    class Meta:
        verbose_name= 'TutoradoReporteSemestralGrupalV2'
        verbose_name_plural= 'TutoradosReportesSemestralesGrupalesV2'
        db_table= 'tutoradoReporteSemestralGrupalV2'
        ordering= ['id']

class ReporteSemestralDepartamentalV2(models.Model):
    archivo = models.CharField(max_length = 200, null = True, blank = True)
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    actividad1 = models.TextField()
    actividad2 = models.TextField()
    actividad3 = models.TextField()
    actividad4 = models.TextField()
    actividad5 = models.TextField()
    actividad6 = models.TextField()
    actividad7 = models.TextField()
    actividad8 = models.TextField()
    actividad9 = models.TextField()
    actividad10 = models.TextField()
    acciones = models.TextField()
    departamento = models.ForeignKey('DepartamentoAcademico', on_delete = models.CASCADE)
    coordinador = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.archivo, self.ano, self.periodo, self.fecha, self.departamento)

    class Meta:
        verbose_name= 'ReporteSemestralDepartamentalV2'
        verbose_name_plural= 'ReportesSemestralesDepartamentalesV2'
        db_table= 'reporteSemestralDepartamentalV2'
        ordering= ['id']

class TutorReporteSemestralDepartamentalV2(models.Model):
    tutoriaGrupal = models.CharField(max_length = 200)
    tutoriaIndividual = models.CharField(max_length = 200)
    estudianteCanalizado = models.TextField()
    areaCanalizada = models.TextField()
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)
    reporte = models.ForeignKey('ReporteSemestralDepartamentalV2', on_delete = models.CASCADE)
    tutor = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.tutoriaGrupal, self.tutoriaIndividual, self.observaciones, self.asistencia, self.grupo)

    class Meta:
        verbose_name= 'TutorReporteSemestralDepartamentalV2'
        verbose_name_plural= 'TutoresReportesSemestralesDepartamentalesV2'
        db_table= 'tutorReporteSemestralDepartamentalV2'
        ordering= ['id']

class ReporteSemestralInstitucionalV2(models.Model):
    archivo = models.CharField(max_length = 200, null = True, blank = True)
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    institucion = models.ForeignKey('Institucion', on_delete = models.CASCADE)
    coordinador = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    class Meta:
        verbose_name= 'ReporteSemestralInstitucionalV2'
        verbose_name_plural= 'ReportesSemestralesInstitucionalesV2'
        db_table= 'reporteSemestralInstitucionalV2'
        ordering= ['id']

class PATDepartamentalV2(models.Model):
    archivo = models.FileField(upload_to = 'CoordinadorTutoriaDepartamentoAcademico/PAT')
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    departamento = models.ForeignKey('DepartamentoAcademico', on_delete = models.CASCADE)
    coordinador = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    class Meta:
        verbose_name= 'PATDepartamentalV2'
        verbose_name_plural= 'PATsDepartamentalesV2'
        db_table= 'patDepartamentalV2'
        ordering= ['id']

class PITInstitucionalV2(models.Model):
    archivo = models.CharField(max_length = 200, null = True, blank = True)
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    institucion = models.ForeignKey('Institucion', on_delete = models.CASCADE)
    jefe = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    class Meta:
        verbose_name= 'PITInstitucionalV2'
        verbose_name_plural= 'PITsInstitucionalesV2'
        db_table= 'pitInstitucionalV2'
        ordering= ['id']

class DiagnosticoInstitucionalV2(models.Model):
    archivo = models.FileField(upload_to = 'CoordinadorInstitucionalTutoria/Diagnostico')
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    institucion = models.ForeignKey('Institucion', on_delete = models.CASCADE)
    coordinador = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)

    class Meta:
        verbose_name= 'DiagnosticoInstitucionalV2'
        verbose_name_plural= 'DiagnosticosInstitucionalesV2'
        db_table= 'diagnosticoInstitucionalV2'
        ordering= ['id']

class ConstanciaTutorV2(models.Model):
    archivo = models.CharField(max_length = 200, null = True, blank = True)
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add = True, editable = False)
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)
    tutor = models.ForeignKey('PersonalTec', on_delete = models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete = models.CASCADE)
    
    class Meta:
        verbose_name= 'ConstanciaTutorV2'
        verbose_name_plural= 'ConstanciasTutoresV2'
        db_table= 'constanciaTutorV2'
        ordering= ['id']

class FechaLimite(models.Model):
    diagnosticoInstitucional = models.DateField()
    planAccionTutorial = models.DateField()
    programaInstitucionalTutorial = models.DateField()
    reporteSemestralGrupal = models.DateField()
    reporteSemestralDepartamental = models.DateField()
    reporteSemestralInstitucional = models.DateField()
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    institucion = models.ForeignKey('Institucion', on_delete = models.CASCADE)
    
    class Meta:
        verbose_name= 'FechaLimite'
        verbose_name_plural= 'FechasLimites'
        db_table= 'fechaLimite'
        ordering= ['id']