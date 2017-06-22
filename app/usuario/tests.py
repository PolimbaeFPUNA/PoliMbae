from django.test import TestCase
from app.usuario.models import Profile
from django.contrib.auth.models import User
# Create your tests here.


class UsuarioTestCase (TestCase):
    '''Crear Pruebas unitarias para Usuario
    1- Se crean 2 registros del modelo User
    2- Se crean 2 perfiles de usuarios '''
    def setUp(self):
        user= User.objects.create(username='prueba', password='prueba')
        user2 = User.objects.create(username='Andres', password='admin')
        user3 = User.objects.create(username='Gloria', password='admin')
        user4 = User.objects.create(username='Legolas', password='arquero')
        p = Profile.objects.create(user=user, cedula='32334', direccion='una calle', telefono='534555')
        p2 = Profile.objects.create(user=user2, cedula='1283', direccion='una calle mas', telefono='474839')

        p3 = Profile.objects.create(user=user3, cedula='4534', direccion='una casa en la quartier', telefono='404945')
        p4 = Profile.objects.create(user=user4, cedula='654321', direccion='bosque encantado', telefono='4993844')

    def test_crear_usuario(self):
        '''Pruebas unitarias para Crear Usuario:
        1- Se crea el registro de User
        2- Se crea el perfil del Usuario
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Crear Usuario')
        print('username: user')
        print('Nombre: user')
        print('password : 789')

        user = User.objects.create(username='user', password='789')
        usuario = Profile.objects.create(user=user, direccion='alguna parte', cedula='587')

        msj = self.assertNotEqual(usuario, [])
        if msj == None:
            print ('\nUsuario ' + usuario.user.username + ' creado exitosamente.\n')

    def test2_crear_usuario(self):
        '''Pruebas unitarias para Crear Usuario:
        1- Se crea el registro de User
        2- Se crea el perfil del Usuario
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Crear Usuario')
        print('username: Mario')
        print('Nombre: Mario')
        print('password : admin')

        user2 = User.objects.create(username='Mario', password='admin')
        usuario2 = Profile.objects.create(user=user2, direccion='Una avenida conocida', cedula='123456')

        msj = self.assertNotEqual(usuario2, [])
        if msj == None:
            print ('\nUsuario ' + usuario2.user.username + ' creado exitosamente.\n')

    def test3_crear_usuario(self):
        '''Pruebas unitarias para Crear Usuario:
        1- Se crea el registro de User
        2- Se crea el perfil del Usuario
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Crear Usuario')
        print('username: Clau')
        print('Nombre: Claudio')
        print('password : pass281')

        user2 = User.objects.create(username='Clau', password='pass281')
        usuario2 = Profile.objects.create(user=user2, direccion='una calle', cedula='8483749')

        msj = self.assertNotEqual(usuario2, [])
        if msj == None:
            print ('\nUsuario ' + usuario2.user.username + ' creado exitosamente.\n')

    def test_modificar_usuario(self):
        '''Pruebas unitarias para Modificar Usuario:
        1- Se trae a una variable 'u' el registro de User
        2- Se modifica el usernama y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.
        Modificacion de Password
        1- Se trae auna variable'u' el registro de Profile de Usuario
        2- Se cambia el password y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.'''
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

    def test4_modificar_usuario(self):
        '''Pruebas unitarias para Modificar Usuario:
        1- Se trae a una variable 'u' el registro de User
        2- Se modifica el usernama y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.
        Modificacion de Password
        1- Se trae auna variable'u' el registro de Profile de Usuario
        2- Se cambia el password y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Modificar Usuario')
        print ('Modificar Username')

        u= Profile.objects.get(user__username='Legolas')
        u.user.username= 'Legolian'
        u.save()

        if self.assertEqual(u.user.username, 'Legolian'):
            print ('Username modificado correctamente')

        print ('Modificar Password')

        u= Profile.objects.get(user__username='Legolas')
        u.user.password= 'arquerogenial'
        u.save()

        if self.assertEqual(u.user.password, 'arquerogenial'):
            print ('Password modificado correctamente')

    def test2_modificar_usuario(self):
        '''Pruebas unitarias para Modificar Usuario:
        1- Se trae a una variable 'u' el registro de User
        2- Se modifica el usernama y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.
        Modificacion de Password
        1- Se trae auna variable'u' el registro de Profile de Usuario
        2- Se cambia el password y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Modificar Usuario')
        print ('Modificar Username')

        u= Profile.objects.get(user__username='Andres')
        u.user.username= 'outre_user'
        u.save()

        if self.assertEqual(u.user.username, 'outre_user'):
            print ('Username modificado correctamente')

        print ('Modificar Password')

        u= Profile.objects.get(user__username='Andres')
        u.user.password= 'outrepass'
        u.save()

        if self.assertEqual(u.user.password, 'outrepass'):
            print ('Password modificado correctamente')

    def test3_modificar_usuario(self):
        '''Pruebas unitarias para Modificar Usuario:
        1- Se trae a una variable 'u' el registro de User
        2- Se modifica el usernama y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.
        Modificacion de Password
        1- Se trae auna variable'u' el registro de Profile de Usuario
        2- Se cambia el password y se guarda en la base de datos
        3- Se notifica en pantalla el exito de la operacion.'''
        print('Modificar Usuario')
        print ('Modificar Username')

        u= Profile.objects.get(user__username='Gloria')
        u.user.username= 'GloriadelaO'
        u.save()

        if self.assertEqual(u.user.username, 'GloriadelaO'):
            print ('Username modificado correctamente')

        print ('Modificar Password')

        u= Profile.objects.get(user__username='Gloria')
        u.user.password= 'unpass'
        u.save()

        if self.assertEqual(u.user.password, 'unpass'):
            print ('Password modificado correctamente')

    def test_crear_doble_user(self):
        '''Pruebas unitarias para Intentar crear un Usuario ya existente:
        1- Se trae a una variable 'user' el registro de User con nombre de username=prueba con el uso de filtros
        2- Si el usuario ya existe, se notifica en pantalla de la existencia del mismo.'''
        print ('Crear doble User')
        print ('prueba')
        user = Profile.objects.filter(user__username='prueba')
        msj = self.assertNotEqual(user, [])
        if msj == None:
            print ('El usuario prueba no fue creado, ya existe en la BD.\n')

    def test_cambiar_password(self):
        '''Pruebas unitarias para Modificar un Usuario ya existente:
              1- Se trae a una variable 'user' el registro de User con nombre de username=prueba con el uso de filtros
              2- Se cambia el pasword del usuario y se guarda en la base de datos
              3- Se notifica en pantalla el exito de la operacion.'''

        user= Profile.objects.get(user__username='prueba')
        user.user.password = '321'
        user.save()

        if self.assertNotEqual(user.user.password, '789'):
            print ('El Password se cambio correctamente')

    def test2_cambiar_password(self):
        '''Pruebas unitarias para Modificar un Usuario ya existente:
              1- Se trae a una variable 'user' el registro de User con nombre de username=Andtres con el uso de filtros
              2- Se cambia el pasword del usuario y se guarda en la base de datos
              3- Se notifica en pantalla el exito de la operacion.'''

        user= Profile.objects.get(user__username='Andres')
        user.user.password = '88430'
        user.save()

        if self.assertNotEqual(user.user.password, '564'):
            print ('El Password se cambio correctamente')

    def test3_cambiar_password(self):
        '''Pruebas unitarias para Modificar un Usuario ya existente:
              1- Se trae a una variable 'user' el registro de User con nombre de username=prueba con el uso de filtros
              2- Se cambia el pasword del usuario y se guarda en la base de datos
              3- Se notifica en pantalla el exito de la operacion.'''

        user= Profile.objects.get(user__username='Legolas')
        user.user.password = '8484843'
        user.save()

        if self.assertNotEqual(user.user.password, '789'):
            print ('El Password se cambio correctamente')


