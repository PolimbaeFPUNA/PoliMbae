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


class UserRol(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200)

    def __unicode__(self):
        return '{} = {}'.format(self.rol_id, self.nombre_rol)


class PermisoRol(models.Model):
    permiso = models.CharField(max_length=150)
    activo = models.BooleanField()
    rol_id = models.ForeignKey(UserRol, null=True, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return '{} = {}'.format(self.rol_id, self.nombre_rol)
