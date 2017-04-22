from django.test import TestCase
from django.test import Client
from app.rol.views import rol_crear
from app.rol.models import Rolusuario
import pytest
import unittest
# Create your tests here.

'''Clase que contendra todas las pruebas para las funciones usadas en el views del app rol'''


class RolTest(TestCase):
    fixtures = ['rol']

    def test_rol_crear(self):
        c = Client()
        print ("Iniciando creacion del Rol")
        respuesta = c.post('/rol/crear/', {'name': 'Administrador General'}, follow=True)
        self.assertEqual(respuesta.status_code, 200)
        print ("Usuario creado con exito \n")
