from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone

class TipoRecurso1(models.Model):
    tipo_id = models.AutoField(primary_key=True)
    nombre_recurso = models.CharField(max_length=80)
    reservable = models.BooleanField(default=True)

    def __unicode__(self):
        return '{}'.format(self.nombre_recurso)

class Caracteristica(models.Model):
    ctra_id = models.AutoField(primary_key=True)
    nombre_caracteristica = models.CharField(max_length=80)
    descripcion = models.TextField(max_length=100, default='')
    tipo_recurso = models.ForeignKey(TipoRecurso1, null=True, blank=True, on_delete = models.CASCADE)

    def __unicode__(self):
        return '{}'.format(self.nombre_caracteristica)


class Recurso1(models.Model):
    recurso_id = models.AutoField(primary_key=True)
    tipo_id = models.ForeignKey(TipoRecurso1, null=True, blank=False, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length= 300, default='')
    Disponible = 'DI'
    Reservado = 'RE'
    EnMantenimiento = 'EM'
    FueradeUso = 'FU'
    EnUso = 'EU'
    ESTADO_CHOICE = ((Disponible, 'Disponible'),
                     (Reservado, 'Reservado'),
                     (EnMantenimiento, 'En Mantenimiento'),
                     (FueradeUso, 'Fuera de Uso'),
                     (EnUso, 'En Uso'),
                     )
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICE, default=Disponible)

    def __unicode__(self):
        return ' {} '.format( self.tipo_id.nombre_recurso)



class DescripCarac(models.Model):
    ctra_id = models.ForeignKey(Caracteristica, null=True, blank=False, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso1, null=True, blank=True, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=100, default='')
    desc_id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return '{}'.format(self.descripcion)



