from django.test import TestCase
from app.usuario.models import Profile, CategoriaUsuario
from django.contrib.auth.models import User
# Create your tests here.

class UsuarioTestCase (TestCase):
    def setUp(self):
        user= User.objects.create(username='prueba', password='prueba')
        categoria= CategoriaUsuario.objects.create(nombre='Alumno')
        Profile.objects.create(user=user, categoria=categoria)

    def test_crear_usuario(self):
        print('Crear Usuario')
        print('username: user')
        print('Nombre: user')
        print('password : 789')

        user = User.objects.create(username='user', password='789')
        usuario = Profile.objects.create(user=user, direccion='alguna parte', categoria='alumno', cedula='587')

        msj = self.assertNotEqual(usuario, [])
        if msj == None:
            print ('\nUsuario ' + usuario.user.username + ' creado exitosamente.\n')

    def test_modificar_usuario(self):
        print('Modificar Usuario')
        print ('Modificar Username')

        u= Profile.objects.get(user__username='prueba')
        u.user.username= 'otro_user'
        u.save()

        if self.assertEqual(u.user.username, 'otro_user'):
            print ('Username modificado correctamente')

        print ('Modificar Password')

        u= Profile.objects.get(user__username='prueba')
        u.user.password= 'otro_pass'
        u.save()

        if self.assertEqual(u.user.password, 'otro_pass'):
            print ('Password modificado correctamente')





