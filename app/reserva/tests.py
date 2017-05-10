from django.test import TestCase
from app.mantenimiento.models import *
from app.recurso.models import *
from app.reserva.models import *
from app.usuario.models import *

# Create your tests here.
class ReservaTestCase(TestCase):
    print('Pruebas de Reservas')

    def setUp(self):
        user=User.objects.create(username='usuario',password='1234')
        usuario=Profile.objects.create(user=user,categoria='categoria')
        recurso=Recurso1.objects.create(recurso_id='1',tipo_id='1')
        ReservaGeneral.objects.create(profile_id=usuario,recurso_id=recurso,fecha_reserva='2017-04-04',hora_inicio='12:00',hora_fin='14:00')


    def test_crear_reserva(self):
        print('\nPrueba: Crear reserva')
        usuario=Profile.objects.get(user='1')
        recurso=Recurso1.objects.get(recurso_id='1')
        reserva=ReservaGeneral.objects.create(profile_id=usuario,recurso_id=recurso,fecha_reserva='2017-04-04',hora_inicio='12:00',hora_fin='14:00')
        msj=self.assertNotEquals(reserva,[])
        if msj==None:
            print('Reserva creada')
"""
    def test_verificar_hora_reserva(self):
        print ('Prueba: verificar hora de reserva')
        reserva=ReservaGeneral.objects.get(recurso_id='1')
        msj=None
        if reserva.recurso==1:
            #self.assertNotEquals(reserva.recurso,2)
            if reserva.fecha_reserva=='2017-04-04':
                #self.assertNotEquals(reserva.fecha_reserva,'2017-04-04')
                if reserva.hora_inicio=='12:00':
                    msj=self.assertNotEquals(reserva.hora_inicio,'12:00')
                if reserva.hora_inicio>'12:00':
                    msj=self.assertGreater(reserva.hora_inicio,'12:00')
                if reserva.hora_fin < '12:00':
                    msj=self.assertGreater('12:00',reserva.hora_fin)
        if msj==None:
            print ('hora de reserva correcta')




"""