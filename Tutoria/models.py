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
    idEstado = models.ForeignKey(Estado, on_delete=models.CASCADE, null = True, blank = True)

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
    idGrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    idEstado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} - {}".format(self.nombre, self.fechaLimite)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cuestionario'
        verbose_name_plural= 'Cuestionarios'
        db_table= 'cuestionario'
        ordering= ['id']