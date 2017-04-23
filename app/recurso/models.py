from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres import fields
from django.utils import timezone


class TipoRecurso(models.Model):
    codigo_tipo = models.IntegerField(default=0)
    nombre_rec = models.CharField(max_length=50)
    reservable = models.BooleanField(default=True)
    fecha_man = models.DateTimeField(default=timezone.now)
    caracteristicas = models.CharField(max_length=200)

# Falta trabajar con los estados predeterminados


class Recurso (models.Model):
    codigo_rec = models.IntegerField(default=0)
    tipo_rec = models.OneToOneField(TipoRecurso, null=True)
    # estados = fields.ArrayField(models.CharField(max_length=20), default=["Disponible",
    #  "Reservado", "En mantenimiento", "Solicitado", "Fuera de uso", "En uso"])
    estado = models.CharField(max_length=50, default="Disponible")
    
    # ["Disponible", "Reservado", "En mantenimiento", "Solicitado", "Fuera de uso", "En uso"]
