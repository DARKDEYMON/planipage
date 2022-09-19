from django.db import models
from django.db.models import Q

# Create your models here.

class Pagina(models.Model):
	nombre = models.CharField(
		null=False,
		blank=False,
		max_length=200
	)
	url = models.URLField(
		null=False,
		blank=False
	)
	def __str__(self):
		return self.nombre

class Tipo(models.Model):
	tipo = models.CharField(
		null=False,
		blank=False,
		max_length=300
	)
	def __str__(self):
		return self.tipo

class Publicacion(models.Model):
	tipo = models.ManyToManyField('noticias.Tipo')
	nombre = models.CharField(
		null=False,
		blank=False,
		max_length=500
	)
	resumen = models.CharField(
		null=True,
		blank=True,
		max_length=500
	)
	contenido = models.TextField(
		null=False,
		blank=False
	)
	publicar = models.BooleanField(
		null=False,
		blank=False,
		default=False
	)
	creado = models.DateTimeField(
		null=False,
		blank=False,
		auto_now_add=True,
	)
	modificado = models.DateTimeField(
		null=False,
		blank=False,
		auto_now=True,
	)
	def solo_fotos(self):
		return Archivo.objects.filter(Q(archivo__icontains='.jpg')|Q(archivo__icontains='.png'), publicacion=self)
	def archivos(self):
		return Archivo.objects.filter(~(Q(archivo__icontains='.jpg')|Q(archivo__icontains='.png')),  publicacion=self)
	def __str__(self):
		return self.nombre

class Archivo(models.Model):
	publicacion = models.ForeignKey('noticias.Publicacion', on_delete=models.CASCADE)
	archivo = models.FileField(
		upload_to='archivos/%Y-%m-%d-%H/',
		null=False,
		blank=False
	)
	def __str__(self):
		return str(self.publicacion)
