from django.test import TestCase
from app.reserva.models import *
from app.usuario.models import *
from app.recurso.models import *
from datetime import date
from django.utils.dateparse import parse_date
# Create your tests here.

class ReservaTestCase(TestCase):
    print ('Tests para Reservas')

    def setUp(self):
        tipo = TipoRecurso1.objects.create(nombre_recurso='Proyector', tipo_id='1')
        recurso = Recurso1.objects.create(recurso_id='1', tipo_id=tipo)
        user = User.objects.create(username='usuario', password='123')
        categoria = CategoriaUsuario.objects.create(nombre='Alumno')
        usuario = Profile.objects.create(user=user, categoria=categoria)
        ReservaGeneral.objects.create(profile=usuario, recurso=recurso, fecha_reserva='2017-05-02', hora_inicio='14:00',
                                      hora_fin='16:00')

    def test_crear_reserva(self):
        print('Prueba: Crear Reserva')
        user= User.objects.get(username='usuario')
        usuario= Profile.objects.get(user=user)
        recurso= Recurso1.objects.get(recurso_id='1')
        reserva= ReservaGeneral.objects.create(profile=usuario, recurso=recurso, fecha_reserva='2017-05-02', hora_inicio='14:00',
                                      hora_fin='16:00')
        msj = self.assertNotEqual(reserva, [])
        if msj == None:
            print ('\nLa reserva se ha registrado exitosamente.\n')

    def test_verificar_hora_reserva(self):
        print ('Prueba: verificar hora de reserva')
        reserva = ReservaGeneral.objects.get(recurso_id='1')
        msj = None
        if reserva.recurso == 1:
            self.assertNotEquals(reserva.recurso, 2)
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

    def test_modificar_reserva(self):
        print ('Prueba: Modificar Reserva')
        reserva= ReservaGeneral.objects.get(recurso_id='1')

        print('Modificar Usuario')
        user = User.objects.create(username='alguien', password='6789')
        categoria = CategoriaUsuario.objects.create(nombre='Titular')
        usuario = Profile.objects.create(user=user, categoria=categoria)
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

    def test_fecha_vieja(self):
        print ('Prueba: Crear una reserva en una fecha en el pasado')
        dia= '2017-06-19'
        day= parse_date(dia)
        if day < date.today():
            self.assertGreater(day, date.today())
        else:
            print('Se ha evitado crear una reserva con una fecha antigua')

