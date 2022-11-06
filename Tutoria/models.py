from pyexpat import model
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Estado(models.Model):
    estado = models.CharField(max_length=100)

    def Mostrar(self):
        return "{}".format(self.estado)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Estado'
        verbose_name_plural= 'Estados'
        db_table= 'estado'
        ordering= ['id']


class Institucion(models.Model):
    nombreInstitucion = models.CharField(max_length=100)
    ruta = models.CharField(max_length=300, blank = True, null = True)

    def Mostrar(self):
        return "{}".format(self.nombreInstitucion)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Institucion'
        verbose_name_plural= 'Instituciones'
        db_table= 'institucion'
        ordering= ['id']


class Grupo(models.Model):
    grupo = models.CharField(max_length=100)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)

    def Mostrar(self):
        return "{}".format(self.grupo)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Grupo'
        verbose_name_plural= 'Grupos'
        db_table= 'grupo'
        ordering= ['id']
    

class DepartamentoAcademico(models.Model):
    departamentoAcademico = models.CharField(max_length=100)
    abreviacion = models.CharField(max_length=10)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} - {}".format(self.departamentoAcademico, self.abreviacion)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'DepartamentoAcademico'
        verbose_name_plural= 'DepartamentosAcademicos'
        db_table= 'departamentoAcademico'
        ordering= ['id']


class PadreMadreTutor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)

    def Mostrar(self):
        return "{} {}, {}".format(self.apellidoPaterno, self.apellidoMaterno, self.nombre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PadreMadreTutor'
        verbose_name_plural= 'PadresMadresTutores'
        db_table= 'padreMadreTutor'
        ordering= ['id']


class Tutorado(models.Model):
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correoPersonal = models.EmailField(max_length = 254)
    semestre = models.PositiveIntegerField()
    idGrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, null = True, blank = True)
    idDepartamentoAcademico = models.ForeignKey('DepartamentoAcademico', on_delete=models.CASCADE)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    idPadreMadreTutor = models.ForeignKey('PadreMadreTutor', on_delete=models.CASCADE, null = True, blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} - {}".format(self.correoPersonal, self.semestre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Tutorado'
        verbose_name_plural= 'Tutorados'
        db_table= 'tutorado'
        ordering= ['id']


class PersonalTec(models.Model):
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correoPersonal = models.EmailField(max_length = 254)
    edificio = models.CharField(max_length=100)
    idDepartamentoAcademico = models.ForeignKey('DepartamentoAcademico', on_delete=models.CASCADE)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)

    def Mostrar(self):
        return "{} - {}".format(self.correoPersonal, self.edificio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PersonalTec'
        verbose_name_plural= 'PersonalTecs'
        db_table= 'personalTec'
        ordering= ['id']


class PersonalMed(models.Model):
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correoPersonal = models.EmailField(max_length = 254)
    edificio = models.CharField(max_length=100)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)

    def Mostrar(self):
        return "{} - {}".format(self.correoPersonal, self.edificio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PersonalMed'
        verbose_name_plural= 'PersonalMeds'
        db_table= 'personalMed'
        ordering= ['id']


class Cuestionario(models.Model):
    nombre = models.CharField(max_length=100)
    fechaPublicado = models.DateField(default=now, editable=False)
    fechaLimite = models.DateField()
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idGrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, null = True, blank = True)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)

    def Mostrar(self):
        return "{} - {}".format(self.nombre, self.idPersonalTec)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cuestionario'
        verbose_name_plural= 'Cuestionarios'
        db_table= 'cuestionario'
        ordering= ['id']


class GrupoRespuesta(models.Model):
    grupoRespuesta = models.CharField(max_length=100)

    def Mostrar(self):
        return "{}".format(self.grupoRespuesta)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'GrupoRespuesta'
        verbose_name_plural= 'GrupoRespuesta'
        db_table= 'grupoRespuesta'
        ordering= ['id']


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=100)
    idGrupoRespuesta = models.ForeignKey('GrupoRespuesta', on_delete=models.CASCADE)
    def Mostrar(self):
        return "{}".format(self.pregunta)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Pregunta'
        verbose_name_plural= 'Preguntas'
        db_table= 'pregunta'
        ordering= ['id']


class Respuesta(models.Model):
    respuesta = models.CharField(max_length=100)
    idGrupoRespuesta = models.ForeignKey('GrupoRespuesta', on_delete=models.CASCADE)
    def Mostrar(self):
        return "{}".format(self.respuesta)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Respuesta'
        verbose_name_plural= 'Respuestas'
        db_table= 'respuesta'
        ordering= ['id']


class RespuestaContestada(models.Model):
    idCuestionario = models.ForeignKey('Cuestionario', on_delete=models.CASCADE)
    idPregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE)
    idRespuesta = models.ForeignKey('Respuesta', on_delete=models.CASCADE)
    idTutorado = models.ForeignKey('Tutorado', on_delete=models.CASCADE)
    def Mostrar(self):
        return "{} - {} - {} - {}".format(self.idCuestionario, self.idPregunta, self.idRespuesta, self.idTutorado)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'RespuestaContestada'
        verbose_name_plural= 'RespuestasContestadas'
        db_table= 'respuestaContestada'
        ordering= ['id']


class PIT(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    fechaLimite = models.DateField()
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PIT'
        verbose_name_plural= 'PITs'
        db_table= 'pit'
        ordering= ['id']


class PAT(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    estadoEdicion = models.CharField(max_length=50)
    fechaLimite = models.DateField()
    idDepartamentoAcademico = models.ForeignKey('DepartamentoAcademico', on_delete=models.CASCADE)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PAT'
        verbose_name_plural= 'PATs'
        db_table= 'pat'
        ordering= ['id']


class ReporteSemestralGrupal(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    fechaLimite = models.DateField()
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idGrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, null = True, blank = True)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ReporteSemestralGrupal'
        verbose_name_plural= 'ReportesSemestralesGrupales'
        db_table= 'reporteSemestralGrupal'
        ordering= ['id']


class ReporteSemestralDepartamento(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    fechaLimite = models.DateField()
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idDepartamentoAcademico = models.ForeignKey('DepartamentoAcademico', on_delete=models.CASCADE)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ReporteSemestralDepartamento'
        verbose_name_plural= 'ReportesSemestralesDepartamentos'
        db_table= 'reporteSemestralDepartamento'
        ordering= ['id']


class ReporteSemestralInstitucional(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    fechaLimite = models.DateField()
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ReporteSemestralInstitucional'
        verbose_name_plural= 'ReportesSemestralesInstitucionales'
        db_table= 'reporteSemestralInstitucional'
        ordering= ['id']


class ConstanciaTutor(models.Model):
    folio = models.CharField(max_length=50)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ConstanciaTutor'
        verbose_name_plural= 'ConstanciaTutores'
        db_table= 'constanciaTutor'
        ordering= ['id']


class Orden(models.Model):
    nombreOrden = models.CharField(max_length=100)
    

    def Mostrar(self):
        return "{} - {}".format(self.nombreOrden)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Orden'
        verbose_name_plural= 'Ordenes'
        db_table= 'orden'
        ordering= ['id']


class Motivo(models.Model):
    nombre = models.CharField(max_length=100)
    idOrden = models.ForeignKey('Orden', on_delete=models.CASCADE)
    

    def Mostrar(self):
        return "{} - {}".format(self.nombre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Motivo'
        verbose_name_plural= 'Motivos'
        db_table= 'motivo'
        ordering= ['id']


class Cita(models.Model):
    folio = models.CharField(max_length=50)
    fecha = models.DateField()
    horaInicio = models.TimeField(null = True, blank = True)
    horaFinal = models.TimeField(null = True, blank = True)
    horaCanalizacion = models.TimeField(null = True, blank = True)
    lugar = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300, null = True, blank = True)
    idMotivo = models.ForeignKey('Motivo', on_delete=models.CASCADE)
    idTutorado = models.ForeignKey('Tutorado', on_delete=models.CASCADE)
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE, null = True, blank = True)
    idPersonalMed = models.ForeignKey('PersonalMed', on_delete=models.CASCADE, null = True, blank = True)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE, null = True, blank = True)
    idOrden = models.ForeignKey('Orden', on_delete=models.CASCADE)
    

    def Mostrar(self):
        return "{} - {}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cita'
        verbose_name_plural= 'Citas'
        db_table= 'cita'
        ordering= ['id']

class Excel(models.Model):  
    control = models.CharField(max_length=8)  
    nombres = models.CharField(max_length=35) 
    apellidos = models.CharField(max_length=35) 
    email = models.EmailField(blank=True)  