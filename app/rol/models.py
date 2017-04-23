from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''Clase para crear el modelo del Rol a ser asignado a los usuarios registrados'''


class Rolusuario(models.Model):
    rol_id = models.CharField(max_length=80, primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)


class Permiso(models.Model):
    permiso = models.CharField(max_length=150)
    activo  = models.BooleanField()
    rol_id = models.ManyToManyField(Rolusuario)

