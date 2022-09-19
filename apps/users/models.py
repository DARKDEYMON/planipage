from django.db import models

# Create your models here.

class Permisos(models.Model):
	class Meta:
		permissions = (
			('users','Permiso al modulo de usuarios'),
			('noticias', 'Permiso al modulo de noticias')
		)
