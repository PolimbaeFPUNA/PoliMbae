from django.test import TestCase
from app.usuario.models import UsuarioUser
from django.contrib.auth.models import User
# Create your tests here.

class UsuarioTestCase (TestCase):
    def setUp(self):
        user= User.objects.create(username='', password='')
        UsuarioUser.objects.create(user=user)

    def test_crear_usuario(self):
        print('\nPrueba')
        print('username: user')
        print('Nombre: user')
        print('password : 789')

        user = User.objects.create(username='user', password='789')
        usuario = UsuarioUser.objects.create(user=user, direccion='alguna parte')

        msj = self.assertNotEqual(usuario, [])
        if msj == None:
            print ('\nUsuario ' + usuario.user.username + ' creado exitosamente.\n')



