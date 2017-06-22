from django.test import TestCase
from app.reserva_new.models import *
from app.usuario.models import *
from app.recurso_pr.models import *
from datetime import date
from django.utils.dateparse import parse_date

# Create your tests here.
class ReservaTestCase(TestCase):
    print ('Tests para Reservas')

    def setUp(self):
        tipo = TipoRecurso1.objects.create(nombre_recurso='Proyector', tipo_id='1')
        recurso = Recurso1.objects.create(recurso_id='1', tipo_id=tipo)
        user = User.objects.create(username='usuario', password='123')
        usuario = Profile.objects.create(user=user)
        tipo2 = TipoRecurso1.objects.create(nombre_recurso='Notebook', tipo_id='2')
        recurso2 = Recurso1.objects.create(recurso_id='2', tipo_id=tipo2)
        reserva = Reserva.objects.create(usuario=usuario, recurso_reservado=recurso, estado_reserva='CONFIRMADA',fecha_reserva='2017-05-02', hora_inicio='14:00',
                                      hora_fin='16:00')
        solicitud = Solicitud.objects.create(usuario=usuario, recurso=recurso, fecha_reserva='2017-05-02', hora_inicio='14:00', hora_fin='16:00')

        reserva2 = Reserva.objects.create(usuario=usuario, recurso_reservado=recurso2, estado_reserva='EN CURSO',
                                         fecha_reserva='2017-05-02', hora_inicio='14:00',
                                         hora_fin='16:00')
        solicitud2 = Solicitud.objects.create(usuario=usuario, recurso=recurso2, fecha_reserva='2017-05-02',
                                             hora_inicio='14:00', hora_fin='16:00')

    def test_crear_solicitud(self):
        print('Prueba: Crear Reserva')
        user = User.objects.get(username='usuario')
        usuario = Profile.objects.get(user=user)
        recurso = Recurso1.objects.get(recurso_id='1')
        solicitud = Solicitud.objects.create(usuario=usuario, recurso=recurso, fecha_reserva='2017-05-02',
                                             hora_inicio='14:00', hora_fin='16:00')

        msj = self.assertNotEqual(solicitud, [])
        if msj == None:
            print ('\nLa solicitud se ha registrado exitosamente.\n')

    def test2_crear_solicitud(self):
        print('Prueba: Crear Reserva')
        user = User.objects.get(username='usuario')
        usuario = Profile.objects.get(user=user)
        recurso2 = Recurso1.objects.get(recurso_id='2')
        solicitud = Solicitud.objects.create(usuario=usuario, recurso=recurso2, fecha_reserva='2017-08-02',
                                             hora_inicio='16:00', hora_fin='20:00')
        msj = self.assertNotEqual(solicitud, [])
        if msj == None:
            print ('\nLa solicitud se ha registrado exitosamente.\n')

    def test_verificar_reserva(self):
        print ('Prueba: verificar hora de reserva')
        reserva = Reserva.objects.get(recurso_reservado='1')
        msj = None
        if reserva.recurso_reservado == 1:
            self.assertNotEquals(reserva.recurso_reservado, 2)
            if reserva.fecha_reserva == '2017-04-04':
                self.assertNotEquals(reserva.fecha_reserva, '2017-04-04')
                if reserva.hora_inicio == '12:00':
                    msj = self.assertNotEquals(reserva.hora_inicio, '12:00')
                if reserva.hora_inicio > '12:00':
                    msj = self.assertGreater(reserva.hora_inicio, '12:00')
                if reserva.hora_fin < '12:00':
                    msj = self.assertGreater('12:00', reserva.hora_fin)
        if msj == None:
            print ('hora de reserva correcta')

    def test2_verificar_reserva(self):
        print ('Prueba: verificar hora de reserva')
        reserva = Reserva.objects.get(recurso_reservado='2')
        msj = None
        if reserva.recurso_reservado == 1:
            self.assertNotEquals(reserva.recurso_reservado, 2)
            if reserva.fecha_reserva == '2017-08-04':
                self.assertNotEquals(reserva.fecha_reserva, '2017-08-04')
                if reserva.hora_inicio == '12:00':
                    msj = self.assertNotEquals(reserva.hora_inicio, '12:00')
                if reserva.hora_inicio > '12:00':
                    msj = self.assertGreater(reserva.hora_inicio, '12:00')
                if reserva.hora_fin < '12:00':
                    msj = self.assertGreater('12:00', reserva.hora_fin)
        if msj == None:
            print ('hora de reserva correcta')

    def test_modificar_reserva(self):
        print ('Prueba: Modificar Reserva')
        reserva= Reserva.objects.get(recurso_reservado='1')

        print('Modificar Usuario')
        user = User.objects.create(username='alguien', password='6789')
        usuario = Profile.objects.create(user=user, cedula='544')
        reserva.profile= usuario
        reserva.save()
        msj = self.assertEquals(reserva.profile.user.username, 'alguien')
        if msj == None:
            print ('\nSe ha modificado el usuario en la reserva.\n')
        print ('Modificar fecha de reserva')
        reserva.fecha_reserva= '2017-05-12'
        reserva.save()
        msj = self.assertEquals(reserva.fecha_reserva, '2017-05-12')
        if msj == None:
            print ('\nSe ha modificado la fecha de la reserva.\n')
        print ('Modificar la hora de inicio y de finalizacion de la reserva')
        reserva.hora_inicio= '18:00'
        reserva.hora_fin= '20:00'
        reserva.save()
        msj = self.assertEquals(reserva.hora_inicio, '18:00')
        if msj == None:
            print ('\nSe ha modificado la hora de inicio de la reserva.\n')
        msj= self.assertEquals(reserva.hora_fin, '20:00')
        if msj== None:
            print('\n Se ha modificado la hora de finalizacion de la reserva')

    def test2_modificar_reserva(self):
        print ('Prueba: Modificar Reserva')
        reserva= Reserva.objects.get(recurso_reservado='2')

        print('Modificar Usuario')
        user = User.objects.create(username='alguien', password='6789')
        usuario = Profile.objects.create(user=user, cedula='544')
        reserva.profile= usuario
        reserva.save()
        msj = self.assertEquals(reserva.profile.user.username, 'alguien')
        if msj == None:
            print ('\nSe ha modificado el usuario en la reserva.\n')
        print ('Modificar fecha de reserva')
        reserva.fecha_reserva= '2017-10-12'
        reserva.save()
        msj = self.assertEquals(reserva.fecha_reserva, '2017-10-12')
        if msj == None:
            print ('\nSe ha modificado la fecha de la reserva.\n')
        print ('Modificar la hora de inicio y de finalizacion de la reserva')
        reserva.hora_inicio= '18:00'
        reserva.hora_fin= '21:00'
        reserva.save()
        msj = self.assertEquals(reserva.hora_inicio, '18:00')
        if msj == None:
            print ('\nSe ha modificado la hora de inicio de la reserva.\n')
        msj= self.assertEquals(reserva.hora_fin, '21:00')
        if msj== None:
            print('\n Se ha modificado la hora de finalizacion de la reserva')

    def test_confirmar_solicitud(self):
        print ('Prueba: Confirmar solicitud')
        solicitud3 = Solicitud.objects.get(recurso_id='1')
        reserva = Reserva.objects.create(usuario=solicitud3.usuario, recurso_reservado=solicitud3.recurso, estado_reserva='CONFIRMADA',
                                         fecha_reserva='2017-05-02', hora_inicio='14:00', hora_fin='16:00')
        msj = self.assertNotEqual(solicitud3, [])
        if msj == None:
            print ('\nLa solicitud se ha registrado exitosamente.\n')

    def test2_confirmar_solicitud(self):
        print ('Prueba: Confirmar solicitud')
        solicitud3 = Solicitud.objects.get(recurso_id='2')
        reserva = Reserva.objects.create(usuario=solicitud3.usuario, recurso_reservado=solicitud3.recurso, estado_reserva='CONFIRMADA',
                                         fecha_reserva='2017-08-02', hora_inicio='16:00', hora_fin='20:00')
        msj = self.assertNotEqual(solicitud3, [])
        if msj == None:
            print ('\nLa solicitud se ha registrado exitosamente.\n')

    def test_entregar_recurso_reserva(self):
        print ('Prueba: Entregar recurso reservado')
        reserva = Reserva.objects.get(recurso_reservado='1')
        reserva.estado_reserva = 'EN CURSO'
        reserva.recurso_reservado.estado = 'EU'
        reserva.save()
        reserva.recurso_reservado.save()
        msj = self.assertNotEqual(reserva, [])
        if msj == None:
            print ('\nLa Entrega del recurso se ha registrado exitosamente.\n')

    def test2_entregar_recurso_reserva(self):
        print ('Prueba: Entregar recurso reservado')
        reserva = Reserva.objects.get(recurso_reservado='2')
        reserva.estado_reserva = 'EN CURSO'
        reserva.recurso_reservado.estado = 'EU'
        reserva.save()
        reserva.recurso_reservado.save()
        msj = self.assertNotEqual(reserva, [])
        if msj == None:
            print ('\nLa Entrega del recurso se ha registrado exitosamente.\n')

