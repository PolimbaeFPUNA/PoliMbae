# -*- coding: utf-8 -*-
'''Modelos del modulo Usuario'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from app.rol.models import Rolusuario


class UsuarioUser(models.Model):
    """ Definición de los atributos de Usuario  """
    user = models.OneToOneField(User)
    cedula = models.IntegerField(default=0)
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    categoria = models.CharField(max_length=50)
    rol = models.ManyToManyField(Rolusuario, default="Usuario Autenticado")

