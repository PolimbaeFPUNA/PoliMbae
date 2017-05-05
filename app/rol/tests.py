from django.test import TestCase, Client
from django.contrib.auth.models import User,Permission,ContentType
from app.rol.models import UserRol
# Create your tests here.
class RolesTestCase(TestCase):

    def setUp(self):
        testuser=User.objects.create_user(username='ivan',password='admin')
        testuser.save()
        cont = ContentType.objects.get_for_model(UserRol)
        self.perm=Permission.objects.create(name='puede crear rol',codename='crear_rol',content_type=cont)
        testuser.user_permissions.add(self.perm)
        testuser.save()
        self.client=Client()

    def test_crear_rol(self):
        '''
        Test para la creacion de un rol
        '''
        self.client.login(username='ivan',password='admin')
        response=self.client.get('/rol/crear/',kwargs={'pk':self.perm.pk})
        print ("crear Rol Usuario")

        self.assertEqual(response.status_code,200)

        self.client.post('rol/crear/',
                         {'name':'Usuario',
                          'permissions':'crear_rol',
                          'crear_from':''})
