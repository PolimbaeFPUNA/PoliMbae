from django.test import TestCase
from app.mantenimiento.models import *
from app.recurso.models import *
from app.reserva.models import *
from app.usuario.models import *
# Create your tests here.

class MantenimientoTestCase(TestCase):

    print('Pruebas para Mantenimiento')
    print ('En la base de datos existe:')
    print ('Tipo de Recurso: Proyector, con id=1')
    print ('Recurso: tipo=Proyector, con id= 1')
    print ('Reserva: sobre el recurso con id=1')

    def setUp(self):
        tipo= TipoRecurso1.objects.create(nombre_recurso='Proyector', tipo_id='1')
        recurso=Recurso1.objects.create(recurso_id='1', tipo_id=tipo)
        Recurso1.objects.create(recurso_id='2', tipo_id=tipo)
        categoria = CategoriaUsuario.objects.create(nombre='Alumno')
        user=User.objects.create(username='usuario', password='123')
        usuario=Profile.objects.create(user=user, categoria=categoria)
        ReservaGeneral.objects.create(profile=usuario, recurso=recurso, fecha_reserva='2017-05-02', hora_inicio='14:00', hora_fin='16:00')
        Mantenimiento.objects.create(recurso=recurso,tipo_recurso=tipo,fecha_entrega='2017-05-02', fecha_fin='2017-05-04', hora_entrega='10:00',
                                     hora_fin='10:00')
    def test_crear_mantenimiento(self):
        print('Prueba: Crear un registro de mantenimiento')
        recurso= Recurso1.objects.get(recurso_id='1')
        tipo= TipoRecurso1.objects.get(tipo_id='1')
        mant = Mantenimiento.objects.create(recurso=recurso,tipo_recurso=tipo,fecha_entrega='2017-05-02', fecha_fin='2017-05-04')
        msj = self.assertNotEqual(mant, [])
        if msj == None:
            print ('\nEl mantenimiento se ha registrado exitosamente.\n')

    def test_reasignar_recurso_reservas(self):
        print('Prueba: reasignar un recurso nuevo a una reserva')
        reserva= ReservaGeneral.objects.get(fecha_reserva='2017-05-02')
        reserva.recurso= Recurso1.objects.get(recurso_id='2')
        msj = self.assertEquals(reserva.recurso.recurso_id, 2)
        if msj == None:
            print ('\nSe ha asignado un nuevo recurso recurso a la reserva.\n')

    def test_modificar_mantenimiento(self):
        print ('Prueba: Modificar un registro de Mantenimiento')
        mant = Mantenimiento.objects.get(recurso__tipo_id='1')
        print ('\n Modificacion: Asignar nuevo recurso')
        mant.recurso= Recurso1.objects.get(recurso_id='2')
        mant.save()
        msj = self.assertEquals(mant.recurso.recurso_id, 2)
        if msj == None:
            print('\n El recurso se ha asignado correctamente')

        print ('\n Modificacion: Asignar nueva fecha de entrega y finalizacion')
        mant.fecha_entrega= '2017-05-04'
        mant.fecha_fin= '2017-05-06'
        mant.save()

        msj = self.assertEquals(mant.fecha_entrega, '2017-05-04')
        if msj == None:
            print('\n La fecha de entrega se ha asignado correctamente')

        msj = self.assertEquals(mant.fecha_fin, '2017-05-06')
        if msj == None:
            print('\n La fecha de finalizacion se ha asignado correctamente')

        print ('\n Modificacion: Asignar nueva hora de entrega y finalizacion')
        mant.hora_entrega = '08:00'
        mant.hora_fin = '08:00'
        mant.save()

        msj = self.assertEquals(mant.hora_entrega, '08:00')
        if msj == None:
            print('\n La hora de entrega se ha asignado correctamente')

        msj = self.assertEquals(mant.hora_fin, '08:00')
        if msj == None:
            print('\n La hora de finalizacion se ha asignado correctamente')

        print ('\n Modificacion: Cambiar el tipo de mantenimiento')
        mant.tipo= 'correctivo'
        mant.save()

        msj = self.assertEquals(mant.tipo, 'correctivo')
        if msj == None:
            print('\n El tipo se ha modificado correctamente')


