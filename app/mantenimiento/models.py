from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils import timezone
from app.recurso_pr.models import Recurso1, TipoRecurso1
from django.utils import timezone


class Mantenimiento(models.Model):
    recurso = models.ForeignKey(Recurso1, default='')
    tipo_recurso = models.ForeignKey(TipoRecurso1, blank=True, default='')
    fecha_entrega = models.DateField()
    fecha_fin = models.DateField()
    hora_entrega = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)
    observacion=models.CharField(max_length=500,default='')
    Pendiente = 'PENDIENTE'
    EnCurso = 'EN CURSO'
    Finalizada = 'FINALIZADA'
    ESTADO_CHOICE = ((Pendiente, 'PENDIENTE'),
                     (EnCurso, 'EN CURSO'),
                     (Finalizada, 'FINALIZADO')
                     )
    estado_mant = models.CharField(max_length=20, choices=ESTADO_CHOICE, default=Pendiente)
    Disponible = 'DI'
    FueradeUso = 'FU'

    EST_CHOICE = ((Disponible, 'Disponible'),
                     (FueradeUso, 'Fuera de Uso'),
                     )
    estado_rec = models.CharField(max_length=2, choices=EST_CHOICE, default=Disponible)
    Preventivo = 'Preventivo'
    Correctivo = 'Correctivo'
    TIPOS = (

        (Preventivo, 'Preventivo'),
        (Correctivo, 'Correctivo'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default='', blank=True)
    def __str__(self):
        return '%s para %s' % (self.recurso_reservado.__str__(),self.usuario.user.username)





