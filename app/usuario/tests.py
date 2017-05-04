from django.test import TestCase
from app.usuario.models import Profile, CategoriaUsuario
from django.contrib.auth.models import User
# Create your tests here.

class UsuarioTestCase (TestCase):
    def setUp(self):
        user= User.objects.create(username='', password='')
        categoria= CategoriaUsuario.objects.create(nombre='Alumno')
        Profile.objects.create(user=user, categoria=categoria)

    def test_crear_usuario(self):
        print('Pruebas para Usuario')
        print('username: user')
        print('Nombre: user')
        print('password : 789')

        user = User.objects.create(username='user', password='789')
        categoria = CategoriaUsuario.objects.create(nombre='Alumno')
        usuario = Profile.objects.create(user=user, direccion='alguna parte', categoria=categoria)

        msj = self.assertNotEqual(usuario, [])
        if msj == None:
            print ('\nUsuario ' + usuario.user.username + ' creado exitosamente.\n')





