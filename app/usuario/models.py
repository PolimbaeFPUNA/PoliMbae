# -*- coding: utf-8 -*-
'''Modelos del modulo Usuario'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from app.rol.models import UserRol
import datetime

class CategoriaUsuario(models.Model):
    Institucional = 'Institucional'
    Titular = 'Titular'
    Adjunto = 'Adjunto'
    Asistente = 'Asistente'
    Encargado_Catedra = 'Encargado de Catedra'
    Auxiliar_Ensenanza = 'Auxiliar de Ensenanza'
    Alumno = 'Alumno'
    Funcionario = 'Funcionario'
    CATEGORIA_CHOICE = ((Institucional, 'Institucional'),
                        (Titular, 'Titular'),
                        (Adjunto, 'Adjunto'),
                        (Asistente, 'Asistente'),
                        (Encargado_Catedra, 'Encargado de Catedra'),
                        (Auxiliar_Ensenanza, 'Auxiliar de Ensenanza'),
                        (Alumno, 'Alumno'),
                        (Funcionario, 'Funcionario'),
                        )
    nombre = models.CharField(max_length=30, choices=CATEGORIA_CHOICE, default=Funcionario)
    prioridad= models.IntegerField(unique=True, default=0)

    def __str__(self):
        return str(self.nombre)


class Profile(models.Model):
    """ Definición de los atributos de Usuario  """
    user = models.OneToOneField(User)
    cedula= models.CharField(max_length=20, default='', unique=True)
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    Institucional = 'Institucional'
    Titular = 'Titular'
    Adjunto = 'Adjunto'
    Asistente = 'Asistente'
    Encargado_Catedra = 'Encargado de Catedra'
    Auxiliar_Ensenanza = 'Auxiliar de Ensenanza'
    Alumno = 'Alumno'
    Funcionario = 'Funcionario'
    CATEGORIA_CHOICE = ((Institucional, 'Institucional'),
                        (Titular, 'Titular'),
                        (Adjunto, 'Adjunto'),
                        (Asistente, 'Asistente'),
                        (Encargado_Catedra, 'Encargado de Catedra'),
                        (Auxiliar_Ensenanza, 'Auxiliar de Ensenanza'),
                        (Alumno, 'Alumno'),
                        (Funcionario, 'Funcionario'),
                        )
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICE, default=Funcionario)
    rol = models.ForeignKey(UserRol,null=True,blank=True, default='')

    def __unicode__(self):
        return '{} '.format(self.user.username)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())


