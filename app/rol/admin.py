from django.contrib import admin
from app.rol.models import Rolusuario
# Register your models here.

'''Registrando el modelo del Rol, para administrarlo con el admin de django'''
admin.site.register(Rolusuario)
