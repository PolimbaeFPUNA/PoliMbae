from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone


class Caracteristica(models.Model):
    ctra_id = models.AutoField(primary_key=True)
    nombre_caracteristica = models.CharField(max_length=80)
    activo = models.BooleanField()

    def __unicode__(self):
        return '{}'.format(self.nombre_caracteristica)


class TipoRecurso1(models.Model):
    tipo_id = models.AutoField(primary_key=True)
    nombre_recurso = models.CharField(max_length=80)
    reservable = models.BooleanField(default=True)
    fecha_mantenimiento = models.DateTimeField(default=timezone.now())
    ctra_id = models.ForeignKey(Caracteristica, null=True, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return '{}'.format(self.nombre_recurso)


class Recurso1(models.Model):
    recurso_id = models.AutoField(primary_key=True)
    tipo_id = models.ForeignKey(TipoRecurso1, null=True, blank=False, on_delete=models.CASCADE)
    Disponible = 'DI'
    Reservado = 'RE'
    EnMantenimiento = 'EM'
    Solicitado = 'SO'
    FueradeUso = 'FU'
    EnUso = 'EU'
    ESTADO_CHOICE = ((Disponible, 'Disponible'),
                     (Reservado, 'Reservado'),
                     (EnMantenimiento, 'En Mantenimiento'),
                     (Solicitado, 'Solicitado'),
                     (FueradeUso, 'Fuera de Uso'),
                     (EnUso, 'En Uso'),
                     )
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICE, default=Disponible)

    def __unicode__(self):
        return '{} = {}'.format(self.estado, self.tipo_id.nombre_recurso)
