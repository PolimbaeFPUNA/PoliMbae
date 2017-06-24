from __future__ import unicode_literals
from app.usuario.models import Profile
from app.recurso_pr.models import Recurso1, TipoRecurso1
from django.db import models
from django.utils import timezone

# Create your models here.

class Solicitud(models.Model):
    solicitud_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso1, null=True, blank=True, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    Pendiente= 'PEN'
    Rechazada= 'RCH'
    ESTADO_SOL = ((Pendiente, 'PEN'),
                  (Rechazada, 'RCH')
                  )
    estado= models.CharField(max_length=3, choices=ESTADO_SOL, default='PEN')
    def __unicode__(self):
        return '{}'.format(self.recurso.tipo_id.nombre_recurso)

    def __str__(self):
        return '%s para %s' % (self.recurso.__str__(),self.usuario.user.username)


class Reserva(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    recurso_reservado = models.ForeignKey(Recurso1, null=True, on_delete=models.CASCADE)
    Confirmada = 'CONFIRMADA'
    Cancelada = 'CANCELADA'
    EnCurso = 'EN CURSO'
    Finalizada= 'FINALIZADA'
    ESTADO_CHOICE = ((Confirmada, 'CONFIRMADA'),
                     (Cancelada, 'CANCELADA'),
                     (EnCurso, 'EN CURSO'),
                     (Finalizada, 'FINALIZADA')
                     )
    estado_reserva = models.CharField(max_length=20, choices=ESTADO_CHOICE)
    fecha_reserva = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def __str__(self):
        return '%s para %s' % (self.recurso_reservado.__str__(),self.usuario.user.username)