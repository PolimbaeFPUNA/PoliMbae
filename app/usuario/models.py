# -*- coding: utf-8 -*-
'''Modelos del modulo Usuario'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from app.rol.models import UserRol
import datetime

class Profile(models.Model):
    """ Definición de los atributos de Usuario  """
    user = models.OneToOneField(User)
    cedula= models.CharField(max_length=20, default='', unique=True)
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    INS = 1
    TIT = 2
    ADJ = 3
    ASI = 4
    ENC = 5
    AUX = 6
    ALU = 7
    FUN = 8
    CATEGORIA_CHOICE = ((INS, 'Institucional'),
                        (TIT, 'Titular'),
                        (ADJ, 'Adjunto'),
                        (ASI, 'Asistente'),
                        (ENC, 'Encargado de Catedra'),
                        (AUX, 'Auxiliar de Ensenanza'),
                        (ALU, 'Alumno'),
                        (FUN, 'Funcionario'),
                        )
    categoria = models.IntegerField(choices=CATEGORIA_CHOICE, default=FUN)
    rol = models.ForeignKey(UserRol,null=True,blank=True, default='')

    def __unicode__(self):
        return '{} '.format(self.user.username)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())


