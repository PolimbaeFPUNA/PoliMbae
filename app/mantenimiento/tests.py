from django.test import TestCase
from app.mantenimiento.models import *
from app.recurso_pr.models import *
from app.reserva_new.models import *
from app.usuario.models import *
# Create your tests here.

class MantenimientoTestCase(TestCase):

    print('Tests para Mantenimiento')
    print ('En la base de datos existe:')
    print ('Tipo de Recurso: Proyector, con id=1')
    print ('Recurso: tipo=Proyector, con id= 1')
    print ('Reserva: sobre el recurso con id=1')

    def setUp(self):
        tipo= TipoRecurso1.objects.create(nombre_recurso='Proyector', tipo_id='1')
        recurso=Recurso1.objects.create(recurso_id='1', tipo_id=tipo)
        Recurso1.objects.create(recurso_id='2', tipo_id=tipo)
        user=User.objects.create(username='usuario', password='123')
        usuario=Profile.objects.create(user=user)
        Reserva.objects.create(usuario=usuario, recurso_reservado=recurso, estado_reserva='CONFIRMADA',
                                         fecha_reserva='2017-05-02', hora_inicio='14:00',
                                         hora_fin='16:00')
        Mantenimiento.objects.create(recurso=recurso,tipo_recurso=tipo,fecha_entrega='2017-05-02', fecha_fin='2017-05-04', hora_entrega='10:00',
                                     hora_fin='10:00')

        tipo2= TipoRecurso1.objects.create(nombre_recurso='Notebook', tipo_id='3')
        recurso2=Recurso1.objects.create(recurso_id='3', tipo_id=tipo2)
        Recurso1.objects.create(recurso_id='4', tipo_id=tipo2)
        Reserva.objects.create(usuario=usuario, recurso_reservado=recurso2, estado_reserva='CONFIRMADA',
                                         fecha_reserva='2017-08-02', hora_inicio='14:00',
                                         hora_fin='16:00')
        Mantenimiento.objects.create(recurso=recurso2, tipo_recurso=tipo2, fecha_entrega='2017-08-02', fecha_fin='2017-08-04', hora_entrega='10:00',
                                     hora_fin='10:00')

        tipo3 = TipoRecurso1.objects.create(nombre_recurso='Sala de Maquinas', tipo_id='5')
        recurso3 = Recurso1.objects.create(recurso_id='5', tipo_id=tipo3)
        Recurso1.objects.create(recurso_id='6', tipo_id=tipo3)
        Reserva.objects.create(usuario=usuario, recurso_reservado=recurso3, estado_reserva='EN CURSO',
                               fecha_reserva='2017-10-02', hora_inicio='14:00',
                               hora_fin='16:00')
        Mantenimiento.objects.create(recurso=recurso3, tipo_recurso=tipo3, fecha_entrega='2017-10-02',
                                     fecha_fin='2017-10-04', hora_entrega='10:00',
                                     hora_fin='10:00')

    def test_crear_mantenimiento(self):
        print('Prueba: Crear un registro de mantenimiento')
        recurso= Recurso1.objects.get(recurso_id='1')
        tipo= TipoRecurso1.objects.get(tipo_id='1')
        mant = Mantenimiento.objects.create(recurso=recurso,tipo_recurso=tipo,fecha_entrega='2017-05-02', fecha_fin='2017-05-04')
        msj = self.assertNotEqual(mant, [])
        if msj == None:
            print ('\nEl mantenimiento se ha registrado exitosamente.\n')

    def test2_crear_mantenimiento(self):
        print('Prueba: Crear un registro de mantenimiento')
        recurso = Recurso1.objects.get(recurso_id='3')
        tipo = TipoRecurso1.objects.get(tipo_id='3')
        mant = Mantenimiento.objects.create(recurso=recurso, tipo_recurso=tipo,fecha_entrega='2017-08-02', fecha_fin='2017-08-04')
        msj = self.assertNotEqual(mant, [])
        if msj == None:
            print ('\nEl mantenimiento se ha registrado exitosamente.\n')

    def test3_crear_mantenimiento(self):
        print('Prueba: Crear un registro de mantenimiento')
        recurso = Recurso1.objects.get(recurso_id='5')
        tipo = TipoRecurso1.objects.get(tipo_id='5')
        mant = Mantenimiento.objects.create(recurso=recurso, tipo_recurso=tipo,fecha_entrega='2017-10-02', fecha_fin='2017-10-04')
        msj = self.assertNotEqual(mant, [])
        if msj == None:
            print ('\nEl mantenimiento se ha registrado exitosamente.\n')

    def test2_reasignar_recurso_reservas(self):
        print('Prueba: reasignar un recurso nuevo a una reserva')
        reserva = Reserva.objects.get(fecha_reserva='2017-08-02')
        reserva.recurso= Recurso1.objects.get(recurso_id='4')
        msj = self.assertEquals(reserva.recurso.recurso_id, 4)
        if msj == None:
            print ('\nSe ha asignado un nuevo recurso recurso a la reserva.\n')

    def test3_reasignar_recurso_reservas(self):
        print('Prueba: reasignar un recurso nuevo a una reserva')
        reserva = Reserva.objects.get(fecha_reserva='2017-10-02')
        reserva.recurso= Recurso1.objects.get(recurso_id='6')
        msj = self.assertEquals(reserva.recurso.recurso_id, 6)
        if msj == None:
            print ('\nSe ha asignado un nuevo recurso recurso a la reserva.\n')

    def test_reasignar_recurso_reservas(self):
        print('Prueba: reasignar un recurso nuevo a una reserva')
        reserva= Reserva.objects.get(fecha_reserva='2017-05-02')
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

    def test_verificar_fecha_hora(self):
        print ('Prueba: Verificar que las fechas y horas del mantenimiento sean correctas')
        print ('recurso: id=1')
        print('fecha de mantenimiento: entrega: 2017-05-02, fin: 2017-05-04')
        print ('hora de mantenimiento: entrega: 10:00, fin: 10:00')

        mant= Mantenimiento.objects.get(recurso__recurso_id='1')

        if mant.fecha_entrega == mant.fecha_fin  and mant.hora_fin < mant.hora_entrega:
            self.assertEquals(mant.fecha_entrega, mant.fecha_fin)
            self.assertGreaterEqual(mant.hora_entrega, mant.hora_fin)
        elif mant.fecha_entrega > mant.fecha_fin:
            self.assertGreater(mant.fecha_entrega, mant.fecha_fin)
        else:
            print('Asignacion de Fechas y Horas correcta')

    def test2_verificar_fecha_hora(self):
        print ('Prueba: Verificar que las fechas y horas del mantenimiento sean correctas')
        print ('recurso: id=3')
        print('fecha de mantenimiento: entrega: 2017-08-02, fin: 2017-08-04')
        print ('hora de mantenimiento: entrega: 10:00, fin: 10:00')

        mant= Mantenimiento.objects.get(recurso__recurso_id='3')

        if mant.fecha_entrega == mant.fecha_fin  and mant.hora_fin < mant.hora_entrega:
            self.assertEquals(mant.fecha_entrega, mant.fecha_fin)
            self.assertGreaterEqual(mant.hora_entrega, mant.hora_fin)
        elif mant.fecha_entrega > mant.fecha_fin:
            self.assertGreater(mant.fecha_entrega, mant.fecha_fin)
        else:
            print('Asignacion de Fechas y Horas correcta')

    def test3_verificar_fecha_hora(self):
        print ('Prueba: Verificar que las fechas y horas del mantenimiento sean correctas')
        print ('recurso: id=5')
        print('fecha de mantenimiento: entrega: 2017-10-02, fin: 2017-10-04')
        print ('hora de mantenimiento: entrega: 10:00, fin: 10:00')

        mant= Mantenimiento.objects.get(recurso__recurso_id='5')

        if mant.fecha_entrega == mant.fecha_fin  and mant.hora_fin < mant.hora_entrega:
            self.assertEquals(mant.fecha_entrega, mant.fecha_fin)
            self.assertGreaterEqual(mant.hora_entrega, mant.hora_fin)
        elif mant.fecha_entrega > mant.fecha_fin:
            self.assertGreater(mant.fecha_entrega, mant.fecha_fin)
        else:
            print('Asignacion de Fechas y Horas correcta')

    def test2_modificar_mantenimiento(self):
        print ('Prueba: Modificar un registro de Mantenimiento')
        mant = Mantenimiento.objects.get(recurso__tipo_id='3')
        print ('\n Modificacion: Asignar nuevo recurso')
        mant.recurso= Recurso1.objects.get(recurso_id='4')
        mant.save()
        msj = self.assertEquals(mant.recurso.recurso_id, 4)
        if msj == None:
            print('\n El recurso se ha asignado correctamente')

        print ('\n Modificacion: Asignar nueva fecha de entrega y finalizacion')
        mant.fecha_entrega= '2017-08-04'
        mant.fecha_fin= '2017-08-06'
        mant.save()

        msj = self.assertEquals(mant.fecha_entrega, '2017-08-04')
        if msj == None:
            print('\n La fecha de entrega se ha asignado correctamente')

        msj = self.assertEquals(mant.fecha_fin, '2017-08-06')
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


    def test3_modificar_mantenimiento(self):
        print ('Prueba: Modificar un registro de Mantenimiento')
        mant = Mantenimiento.objects.get(recurso__tipo_id='5')
        print ('\n Modificacion: Asignar nuevo recurso')
        mant.recurso= Recurso1.objects.get(recurso_id='6')
        mant.save()
        msj = self.assertEquals(mant.recurso.recurso_id, 6)
        if msj == None:
            print('\n El recurso se ha asignado correctamente')

        print ('\n Modificacion: Asignar nueva fecha de entrega y finalizacion')
        mant.fecha_entrega= '2017-10-04'
        mant.fecha_fin= '2017-10-06'
        mant.save()

        msj = self.assertEquals(mant.fecha_entrega, '2017-10-04')
        if msj == None:
            print('\n La fecha de entrega se ha asignado correctamente')

        msj = self.assertEquals(mant.fecha_fin, '2017-10-06')
        if msj == None:
            print('\n La fecha de finalizacion se ha asignado correctamente')

        print ('\n Modificacion: Asignar nueva hora de entrega y finalizacion')
        mant.hora_entrega = '08:00'
        mant.hora_fin = '10:00'
        mant.save()

        msj = self.assertEquals(mant.hora_entrega, '08:00')
        if msj == None:
            print('\n La hora de entrega se ha asignado correctamente')

        msj = self.assertEquals(mant.hora_fin, '10:00')
        if msj == None:
            print('\n La hora de finalizacion se ha asignado correctamente')

        print ('\n Modificacion: Cambiar el tipo de mantenimiento')
        mant.tipo= 'preventivo'
        mant.save()

        msj = self.assertEquals(mant.tipo, 'preventivo')
        if msj == None:
            print('\n El tipo se ha modificado correctamente')
