from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from django.db.models.fields.files import ImageField
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
# Create your models here.


class Servicio (models.Model):
    nombre = models.CharField(max_length = 50)
    descripcion = models.TextField()
    
    def __unicode__(self):
        return self.nombre
    
    
class Evento (models.Model):
    nombre = models.CharField(max_length = 50)
    empresa = models.CharField(max_length = 50)
    PUBLICO = 'Publico'
    PRIVADO = 'Privado'
    TIPOS = ( (PUBLICO,'Publico'),(PRIVADO,'Privado'), )
    tipo = models.CharField(max_length = 7, choices = TIPOS, default = PUBLICO)
    servicios = models.ManyToManyField(Servicio)
    activo = models.BooleanField(default = True)
    
    def __unicode__(self):
        return "{0} / {1}".format(self.nombre, self.tipo)
    

class Empresa (models.Model):
    nombre = models.CharField(max_length = 50)
    descripcion = models.TextField()
    logo = models.ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    evento = models.ForeignKey( Evento, related_name = 'evento_asociado')
    
    def __unicode__(self):
        return self.nombre   
        
class MuestraComercial (models.Model):
    nombre_empresa = models.CharField(max_length = 50)
    logo = models.ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    stand = models.IntegerField()
    hipervinculo =  models.CharField(max_length = 100)
    email = models.CharField(max_length= 50)
    evento = models.ForeignKey(Evento)
    
    def __unicode__(self):
        return "{0} / Web: {1} / Contacto: {2}".format(self.nombre_empresa,self.hipervinculo,self.email)
    
    class Meta(object):
        verbose_name = 'Muestra Comercial'
        verbose_name_plural = 'Muestras Comerciales'
 
class Categoria (models.Model):
    nombre = models.CharField(max_length = 50) 
    descripcion = models.TextField()
    
    def __unicode__(self):
        return self.nombre
    
class Actividad (models.Model):
    ABIERTA = 'Abierta'
    CERRADA = 'Cerrada'
    TIPOI = 'Tipo 1'
    TIPOII = 'Tipo 2'
    TIPOS = ( (TIPOI,'Tipo 1'),(TIPOII,'Tipo 2'), )
    evento = models.ForeignKey(Evento)
    tipo = models.CharField(max_length = 7, choices = TIPOS, default = TIPOI)
    nombre = models.CharField(max_length = 150)
    persona = models.CharField(max_length = 100)
    CARACTER=  ( (ABIERTA,'Abierta'),(CERRADA,'Cerrada'), )
    caracter = models.CharField(max_length = 7, choices = CARACTER, default = ABIERTA)
    cupos = models.IntegerField(default = 0)
    informacion= models.TextField()
    imagen = ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin= models.TimeField()
    categorias = models.ManyToManyField(Categoria)
    servicios = models.ManyToManyField(Servicio)
    
    def __unicode__(self):
        return "{0}, {1}".format(self.nombre, self.evento.nombre)
    
    class Meta(object):
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['fecha_inicio','hora_inicio']
    
class RutaAudio(models.Model):
    actividad = models.ForeignKey(Actividad)
    INGLES = 'Ingles'
    ESPANOL = 'Espanol'
    FRANCES = 'Frances'
    IDIOMAS = ( (INGLES,'Ingles'),(ESPANOL,'Espanol'),(FRANCES, 'Frances') )
    idioma = models.CharField(max_length = 15, choices = IDIOMAS, default = INGLES)
    url_android = models.CharField(max_length = 80)
    url_ios = models.CharField(max_length = 80)
    
class PuntoControl (models.Model):
    nombre = models.CharField(max_length = 50)
    usuario = models.OneToOneField(User)
    actividades = models.ManyToManyField(Actividad, related_name = "actividades")
    evento = models.ForeignKey(Evento)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta(object):
        verbose_name = 'Punto de Control'
        verbose_name_plural = 'Puntos de Control'

class Pregunta (models.Model):
    actividad = models.ForeignKey(Actividad)
    texto = models.TextField()
    
    
    def __unicode__(self):
        return self.texto
    
class Opcion (models.Model):
    numeral = models.CharField(max_length = 2)
    texto = models.CharField(max_length = 50)
    votos = models.IntegerField(default = 0)
    pregunta = models.ForeignKey(Pregunta)
    
    def __unicode__(self):
        return "{0}) {1} | votos: {2}".format(self.numeral, self.texto, self.votos)
    
    class Meta(object):
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'
    
class Patrocinador (models.Model):
    nombre = models.CharField(max_length = 50)
    baner = models.ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    hipervinculo = models.URLField()
    logo = models.ImageField(help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    
    def __unicode__(self):
        return self.nombre
    
    class Meta(object):
        verbose_name = 'Patrocinador'
        verbose_name_plural = 'Patrocinadores'
 
class Informacion (models.Model):
    evento = models.OneToOneField(Evento)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    localizacion = GeopositionField(default = '4.7,-74')
    patrocinadores = models.ManyToManyField(Patrocinador)
    logo = models.ImageField(help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')

    
    def __unicode__(self):
        return "{0}, desde: {1}, hasta: {2}".format(self.evento.nombre, self.fecha_inicio, self.fecha_fin)
    
    class Meta(object):
        verbose_name = 'Informacion del evento'
        verbose_name_plural = 'Informacion del Evento'   
        
class Memoria (models.Model):
    nombre = models.CharField(max_length = 50)
    archivo = models.FileField(help_text='Soporta archivos en formato DOCX,PDF,PPT,XML')
    descripcion = models.TextField()
    actividad = models.ForeignKey(Actividad)
    
    def __unicode__(self):
        return self.nombre
    
  
class Asistente (models.Model):
    nombre = models.CharField(max_length = 50)
    MASCULINO = 'Masculino'
    FEMENINO = 'Femenino'
    GENEROS = ( (MASCULINO,'Masculino'),(FEMENINO,'Femenino'), )
    genero = models.CharField(max_length = 10, choices = GENEROS, default = MASCULINO )
    apellido = models.CharField(max_length = 100)
    celular = models.CharField(max_length = 11)
    email = models.EmailField()
    empresa = models.ForeignKey(Empresa, null = True, blank = True, default = None)
    cargo = models.CharField(max_length = 50)
    foto = models.ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP')
    activo = models.BooleanField(default = True)
    eventos = models.ManyToManyField(Evento)
    actividades = models.ManyToManyField(Actividad)
    categoria = models.ForeignKey(Categoria,null = True, blank = True, default = None)
    imagen = ImageField( help_text='Soporta archivos en formato JPEG,JPG,PNG,BMP', null = True, blank = True, default = None)
    
    @classmethod
    def create(cls, nombre, apellido, celular, cargo,foto, genero):
        asistente = cls(nombre = nombre,apellido = apellido,celular = celular, cargo = cargo, foto = foto, genero = genero)
        asistente.save()
        return asistente
    
    
    def __unicode__(self):
        return "{0} {1}".format(self.nombre, self.apellido)
    

    
class Asistente_Ingresado(models.Model):
    asistente = models.ForeignKey(Asistente)
    actividad = models.ForeignKey(Actividad)
    ingresado = models.BooleanField(default = False)
    traduccion = models.BooleanField(default = False)
    fecha_hora = models.DateTimeField()
    
    @classmethod
    def create(cls, asistente, actividad, ingresado):
        asistente_ingresado = cls(asistente = asistente,actividad = actividad, ingresado = ingresado)
        asistente_ingresado.fecha_hora = timezone.now()
        asistente_ingresado.save()
        return asistente_ingresado
    
    def __unicode__(self):
        return "{0} - {1} - {2}".format(self.asistente.nombre, self.actividad.nombre,self.ingresado)
    
    
    
class Perfil(models.Model):
    ADMINISTRADOR = 1
    SOPORTE_TECNICO = 2
    PUNTO_CONTROL = 3
    
    OPCIONES_ROL = (
                    (ADMINISTRADOR, 'Administrador'),
                    (SOPORTE_TECNICO, 'Soporte Tecnico'),
                    (PUNTO_CONTROL, 'Punto de control'),
                    )
    
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    asistente = models.OneToOneField(Asistente, on_delete=models.CASCADE, null = True, blank = True)
    rol = models.IntegerField(choices = OPCIONES_ROL)
    evento = models.ForeignKey(Evento, on_delete = models.CASCADE)
    
    @classmethod
    def create(cls, usuario, asistente,rol, evento):
        perfil = cls(usuario = usuario, asistente = asistente,rol = rol, evento = evento)
        perfil.save()
        return perfil
    
    def __unicode__(self):
        return "{0} - {1}".format(self.usuario.first_name, self.rol)
    
    class Meta(object):
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfil'
    
class Duda (models.Model):
    texto = models.TextField()
    respondida = models.BooleanField(default = False)
    actividad = models.ForeignKey(Actividad)
    asistente = models.ForeignKey(Asistente)
    
    def __unicode__(self):
        return self.texto
    
    @classmethod
    def create(cls, texto, actividad, asistente):
        duda =  cls(texto = texto, actividad = actividad, asistente = asistente)
        duda.save()
        return duda
    
    
    