from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''Clase para crear el modelo del Rol a ser asignado a los usuarios registrados'''

class Rolusuario(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=50)
    crear_usuario = models.NullBooleanField(default=False)
    modificar_usuario = models.NullBooleanField(default=False)
    eliminar_usuario = models.NullBooleanField(default=False)
    crear_rol = models.NullBooleanField(default=False)
    modificar_rol = models.NullBooleanField(default=False)
    eliminar_rol = models.NullBooleanField(default=False)
    crear_recurso = models.NullBooleanField(default=False)
    modificar_recurso = models.NullBooleanField(default=False)
    eliminar_recurso = models.NullBooleanField(default=False)
    consultar_recurso = models.NullBooleanField(default=False)
    crear_reserva = models.NullBooleanField(default=False)
    modificar_reserva = models.NullBooleanField(default=False)
    eliminar_reserva = models.NullBooleanField(default=False)
    consultar_reserva = models.NullBooleanField(default=False)
    crear_mantenimiento = models.NullBooleanField(default=False)
    modificar_mantenimiento = models.NullBooleanField(default=False)
    eliminar_mantenimiento = models.NullBooleanField(default=False)
