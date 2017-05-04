from __future__ import unicode_literals
from app.usuario.models import Profile
from app.recurso.models import Recurso1
from django.db import models
from django.utils import timezone

# Create your models here.


class ReservaGeneral(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso1, null=True, blank=False, on_delete=models.CASCADE)
    fecha_reserva = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def __unicode__(self):
        return '{} , {}'.format(self.recurso.estado,
                                self.recurso.tipo_id.nombre_recurso)

    def get_reserva_id(self):
        return self.reserva_id

    def get_profile(self):
        return self.profile.cedula

    def get_recurso(self):
        return self.recurso_id

    def get_fecha_reserva(self):
        return self.fecha_reserva

    def geet_hora_inicio(self):
        return self.hora_inicio

    def geet_hora_fin(self):
        return self.hora_fin

    def __iter__(self):
        return [
            self.reserva_id,
            self.profile,
            self.recurso,
            self.fecha_reserva,
            self.hora_inicio,
            self.hora_fin
        ]


class ListaReservaGeneral(models.Model):
    lista_id = models.AutoField(primary_key=True)
    recurso_reservado = models.IntegerField()
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
    estado_reserva = models.CharField(max_length=2, choices=ESTADO_CHOICE, default=Disponible)
    fecha_reserva = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def get_lista_id(self):
        return self.lista_id

    def get_recurso_reservado(self):
        return self.recurso_reservado

    def get_estado_reserva(self):
        return self.estado_reserva

    def get_fecha_reserva(self):
        return self.fecha_reserva

    def get_hora_inicio(self):
        return self.hora_inicio

    def get_hora_fin(self):
        return self.hora_fin

    def __iter__(self):
        return [
            self.lista_id,
            self.recurso_reservado,
            self.estado_reserva,
            self.fecha_reserva,
            self.hora_inicio,
            self.hora_fin
        ]


class ReservaEspecifica(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso1, null=True, blank=False, on_delete=models.CASCADE)
    fecha_reserva = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def __unicode__(self):
        return '{} , {}'.format(self.recurso.estado,
                                self.recurso.tipo_id.nombre_recurso)

    def get_reserva_id(self):
        return self.reserva_id

    def get_profile(self):
        return self.profile

    def get_recurso(self):
        return self.recurso_id

    def get_fecha_reserva(self):
        return self.fecha_reserva

    def geet_hora_inicio(self):
        return self.hora_inicio

    def geet_hora_fin(self):
        return self.hora_fin

    def __iter__(self):
        return [
            self.reserva_id,
            self.profile,
            self.recurso,
            self.fecha_reserva,
            self.hora_inicio,
            self.hora_fin
        ]


class ListaReservaEspecifica(models.Model):
    lista_id = models.AutoField(primary_key=True)
    recurso_reservado = models.IntegerField()
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
    estado_reserva = models.CharField(max_length=2, choices=ESTADO_CHOICE, default=Disponible)
    prioridad = models.IntegerField()
    fecha_reserva = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def get_lista_id(self):
        return self.lista_id

    def get_recurso_reservado(self):
        return self.recurso_reservado

    def get_estado_reserva(self):
        return self.estado_reserva

    def get_prioridad(self):
        return self.prioridad

    def get_fecha_reserva(self):
        return self.fecha_reserva

    def get_hora_inicio(self):
        return self.hora_inicio

    def get_hora_fin(self):
        return self.hora_fin

    def __iter__(self):
        return [
            self.lista_id,
            self.recurso_reservado,
            self.estado_reserva,
            self.prioridad,
            self.fecha_reserva,
            self.hora_inicio,
            self.hora_fin
        ]
