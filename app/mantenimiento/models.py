from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils import timezone
from app.recurso.models import Recurso1, TipoRecurso1
from django.utils import timezone


class Mantenimiento(models.Model):
    recurso= models.ForeignKey(Recurso1, default='')
    tipo_recurso= models.ForeignKey(TipoRecurso1, blank=True, default='')
    fecha_entrega= models.DateField()
    fecha_fin = models.DateField()
    hora_entrega= models.TimeField(default=timezone.now)
    hora_fin=models.TextField(default=timezone.now)
    Preventivo= 'P'
    Correctivo= 'C'
    TIPOS = (

        (Preventivo, 'Preventivo'),
        (Correctivo, 'Correctivo'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default='', blank=True)
    Funcional = 'FUN'
    NoFuncional = 'NF'
    Pendiente= 'PEN'
    RESULTADO = (
        (Funcional, 'Funcional'),
        (NoFuncional, 'No Funcional'),
        (Pendiente, 'Pendiente')
    )
    resultado = models.CharField(max_length=20, choices=RESULTADO, default='', blank=True)




