from django.test import TestCase, Client
from django.contrib.auth.models import User,Permission,ContentType
from app.rol.models import UserRol
# Create your tests here.


class RolesTestCase(TestCase):

    def setUp(self):
        testuser=User.objects.create_user(username='ivan',password='admin')
        testuser.save()
        testuser2 = User.objects.create_user(username='maria', password='admin')
        testuser2.save()

        cont = ContentType.objects.get_for_model(UserRol)
        self.perm=Permission.objects.create(name='puede crear rol',codename='add_permissions',content_type=cont)
        testuser.user_permissions.add(self.perm)
        testuser.save()

        testuser2.user_permissions.add(self.perm)
        testuser2.save()

        self.client = Client()

    def test_crear_rol(self):
        '''
        Test para la creacion de un rol
        '''
        self.client.login(username='ivan',password='admin')
        response=self.client.get('/rol/crear/',kwargs={'pk':self.perm.pk})
        print ("crear Rol Usuario")

        self.assertNotEqual(response.status_code,200)

        self.client.post('rol/crear/',
                         {'name':'Usuario',
                          'permissions':'crear_rol',
                          'crear_from':''})

    def test_crear_rol2(self):
        '''
        Test para la creacion de un rol
        '''
        self.client.login(username='maria',password='admin')
        response=self.client.get('/rol/crear/',kwargs={'pk':self.perm.pk})
        print ("crear Rol Usuario")

        self.assertNotEqual(response.status_code,200)

        self.client.post('rol/crear/',
                         {'name':'Usuario',
                          'permissions':'crear_rol',
                          'crear_from':''})

