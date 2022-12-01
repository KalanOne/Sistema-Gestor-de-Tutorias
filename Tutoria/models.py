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
    opciones=(
            (1, 1),
            (2, 2),
            (3, 3)
    )

    nombreInstitucion = models.CharField(max_length=100)
    ruta = models.CharField(max_length=300, blank = True, null = True)
    anoActual = models.IntegerField()
    periodoActual = models.IntegerField(choices = opciones)

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
    opciones=(
            ('A','A'),
            ('B','B'),
            ('C','C')
    )   
    grupo = models.CharField(max_length=100, blank=True, null=True, choices = opciones)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE, null = True, blank = True)
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE, null = True, blank = True)
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
    apellidos = models.CharField(max_length=100)
    telefonotutor = models.CharField(max_length=10)

    def Mostrar(self):
        return "{}, {}".format(self.apellidos, self.nombre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PadreMadreTutor'
        verbose_name_plural= 'PadresMadresTutores'
        db_table= 'padreMadreTutor'
        ordering= ['id']


class Tutorado(models.Model):
    domicilio = models.CharField(max_length=100, blank = True)
    telefono = models.CharField(max_length=10, blank = True)
    correoPersonal = models.EmailField(max_length = 254, blank = True)
    semestre = models.PositiveIntegerField(blank = True)
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
    domicilio = models.CharField(max_length=100, blank = True)
    telefono = models.CharField(max_length=10, blank = True)
    correoPersonal = models.EmailField(max_length = 254, blank = True)
    edificio = models.CharField(max_length=100, blank = True)
    idDepartamentoAcademico = models.ForeignKey('DepartamentoAcademico', on_delete=models.CASCADE, null = True, blank = True)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    archivo = models.FileField(upload_to = 'Cuestionarios/Asignacion/%Y/%m/%d')
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE)
    idGrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} - {}".format(self.nombre, self.idPersonalTec)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cuestionario'
        verbose_name_plural= 'Cuestionarios'
        db_table= 'cuestionario'
        ordering= ['id']


class CuestionarioContestado(models.Model):
    archivo = models.FileField(upload_to = 'Cuestionarios/Respuesta/%Y/%m/%d')
    idCuestionario = models.ForeignKey('Cuestionario', on_delete=models.CASCADE)
    idTutorado = models.ForeignKey('Tutorado', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} - {} - {}".format(self.idTutorado_id, self.idCuestionario_id, self.archivo)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'CuestionarioContestado'
        verbose_name_plural= 'CuestionarioContestados'
        db_table= 'cuestionarioContestado'
        ordering= ['id']


class Orden(models.Model):
    nombreOrden = models.CharField(max_length=100)
    

    def Mostrar(self):
        return "{}".format(self.nombreOrden)

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
        return "{}".format(self.nombre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Motivo'
        verbose_name_plural= 'Motivos'
        db_table= 'motivo'
        ordering= ['id']


class Cita(models.Model):
    folio = models.CharField(max_length=50)
    fechaSolicitud = models.DateField(auto_now_add = True, editable = False)
    fechaAsignacion = models.DateField(null = True, blank = True)
    fechaCita = models.DateField(null = True, blank = True)
    horaInicio = models.TimeField(null = True, blank = True)
    horaFinal = models.TimeField(null = True, blank = True)
    horaCanalizacion = models.TimeField(null = True, blank = True)
    lugar = models.CharField(max_length=50, null = True, blank = True)
    descripcion = models.TextField(null = True, blank = True)
    idMotivo = models.ForeignKey('Motivo', on_delete=models.CASCADE)
    idTutorado = models.ForeignKey('Tutorado', on_delete=models.CASCADE)
    idPersonalTec = models.ForeignKey('PersonalTec', on_delete=models.CASCADE, null = True, blank = True)
    idPersonalMed = models.ForeignKey('PersonalMed', on_delete=models.CASCADE, null = True, blank = True)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    idOrden = models.ForeignKey('Orden', on_delete=models.CASCADE)
    idInstitucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    

    def Mostrar(self):
        return "{}".format(self.folio)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cita'
        verbose_name_plural= 'Citas'
        db_table= 'cita'
        ordering= ['id']


class Credito(models.Model):
    nombre_doc = models.CharField(max_length=100, null = True, blank = True)
    archivo = models.FileField(upload_to = 'Tutorado/Creditos')
    comentarios = models.CharField(max_length=200, null = True, blank = True)
    idEstado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    idTutorado = models.ForeignKey('Tutorado', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{}".format(self.idTutorado)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Credito'
        verbose_name_plural= 'Creditos'
        db_table= 'credito'
        ordering= ['id']


class registrarAlumno(models.Model):  
    control = models.CharField(max_length=8)  
    nombres = models.CharField(max_length=35) 
    apellidos = models.CharField(max_length=35) 
    email = models.EmailField(blank=True)  
    semestre = models.IntegerField()

    def Mostrar(self):
        return "{} - {}".format(self.nombres, self.apellidos)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'registrarAlumno'
        verbose_name_plural= 'registrarAlumnos'
        db_table= 'registrarAlumno'
        ordering= ['id']

class registrarPersonalTec(models.Model):  
    username = models.CharField(max_length=30)   
    nombres = models.CharField(max_length=35) 
    apellidos = models.CharField(max_length=35) 
    email = models.EmailField(blank=True)

    def Mostrar(self):
        return "{} - {}".format(self.nombres, self.apellidos)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'registrarPersonalTec'
        verbose_name_plural= 'registrarPersonalTecs'
        db_table= 'registrarPersonalTec'
        ordering= ['id']