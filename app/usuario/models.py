# -*- coding: utf-8 -*-
'''Modelos del modulo Usuario'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from app.rol.models import UserRol


class CategoriaUsuario(models.Model):
    nombre= models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre)





class Profile(models.Model):
    """ Definición de los atributos de Usuario  """
    user = models.OneToOneField(User)
    cedula= models.CharField(max_length=20, default='')
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    categoria = models.ForeignKey(CategoriaUsuario, blank=True, default='')
    #rol = models.ForeignKey(UserRol,null=True,blank=True, default='')



    def __unicode__(self):
        return '{} '.format(self.cedula)




