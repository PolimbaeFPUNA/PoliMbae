from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from app.recurso_pr.models import *
from datetime import date
# Create your tests here.


class RecursoTestCase(TestCase):
    print ('\nTests para Recurso ')

    def setUp(self):
        tipo= TipoRecurso1.objects.create(nombre_recurso='Proyector', reservable= True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        Caracteristica.objects.create(nombre_caracteristica='marca', tipo_recurso=tipo)
        tipo = TipoRecurso1.objects.create(nombre_recurso='Notebook', reservable=True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Sala de Maquina', reservable=True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Equipo de Sonido', reservable=True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Laboratorio de Electricidad', reservable=True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        tipo = TipoRecurso1.objects.create(nombre_recurso='DROM', reservable=True)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Camara digital', reservable=False)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')

    def test_crear_tipo_recurso(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Notebook', reservable=True)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test11_crear_tipo_recurso(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Camara digital', reservable=False)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test_crear_tipo_recurso2(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Sala de Maquina', reservable=True)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test_crear_tipo_recurso3(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Equipo de Sonido', reservable=False)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test_crear_tipo_recurso4(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='Laboratorio de Electricidad', reservable=False)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test_crear_tipo_recurso5(self):
        print('Prueba: Crear Tipo de Recurso')
        tipo = TipoRecurso1.objects.create(nombre_recurso='DROM', reservable=False)
        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')

    def test_crear_recurso3(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='Sala de Maquina')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test_crear_recurso4(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='Equipo de Sonido')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test_crear_recurso9(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='Notebook')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test_crear_recurso5(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='Laboratorio de Electricidad')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test11_crear_recurso(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='Camara digital')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test_crear_recurso6(self):
        print('Prueba: Crear Recurso')
        try:
            tipo = TipoRecurso1.objects.get(nombre_recurso='DROM')
            recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test_modificar_recurso(self):
        print ('Prueba: Modificar Recurso')
        recurso= Recurso1.objects.get(tipo_id__nombre_recurso='Proyector')
        print('Modificar estado del recurso')
        recurso.estado= 'RE'
        recurso.save()
        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_recurso2(self):
        print ('Prueba: Modificar Recurso')
        try:
            recurso= Recurso1.objects.get(tipo_id__nombre_recurso='Notebook')
            print('Modificar estado del recurso')
            recurso.estado = 'RE'
            recurso.save()
        except Recurso1.DoesNotExist:
            recurso = None
            print('El Tipo de Recurso no se encuentra')

        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_recurso3(self):
        print ('Prueba: Modificar Recurso')
        try:
            recurso = Recurso1.objects.get(tipo_id__nombre_recurso='Sala de Maquina')
            print('Modificar estado del recurso')
            recurso.estado = 'RE'
            recurso.save()
        except Recurso1.DoesNotExist:
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_recurso4(self):
        print ('Prueba: Modificar Recurso')
        try:
            recurso = Recurso1.objects.get(tipo_id__nombre_recurso='Equipo de Sonido')
            print('Modificar estado del recurso')
            recurso.estado = 'RE'
            recurso.save()
        except Recurso1.DoesNotExist:
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_recurso5(self):
        print ('Prueba: Modificar Recurso')
        try:
            recurso = Recurso1.objects.get(tipo_id__nombre_recurso='Laboratorio de Electricidad')
            print('Modificar estado del recurso')
            recurso.estado = 'RE'
            recurso.save()
        except Recurso1.DoesNotExist:
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_recurso6(self):
        print ('Prueba: Modificar Recurso')
        try:
            recurso = Recurso1.objects.get(tipo_id__nombre_recurso='DROM')
            print('Modificar estado del recurso')
            recurso.estado = 'RE'
            recurso.save()
        except Recurso1.DoesNotExist:
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(recurso.estado, 'RE'):
            print ('Se ha modificado el estado del recurso exitosamente')

    def test_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo= TipoRecurso1.objects.get(nombre_recurso='Proyector')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso= 'Sala'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'Sala'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable= False
        tipo.save()
        if not self.assertEquals(tipo.reservable, False):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test2_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        try:
            tipo= TipoRecurso1.objects.get(nombre_recurso='Notebook')
            print ('Modificar Nombre del Tipo de Recurso')
            tipo.nombre_recurso = 'Computadora de Escritorio'
            tipo.save()
        except TipoRecurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(tipo.nombre_recurso, 'Computadora de Escritorio'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        try:
            tipo.reservable = False
            tipo.save()
        except Recurso1.DoesNotExist:
            tipo =None
            recurso = None
            print('El Tipo de Recurso no se encuentra')
        if not self.assertEquals(tipo.reservable, False):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test3_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo= TipoRecurso1.objects.get(nombre_recurso='Equipo de Sonido')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso = 'Parlante Portatil'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'Parlante Portatil'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable = True
        tipo.save()
        if not self.assertEquals(tipo.reservable, True):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test11_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo= TipoRecurso1.objects.get(nombre_recurso='Camara digital')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso = 'Visor'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'Visor'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable = True
        tipo.save()
        if not self.assertEquals(tipo.reservable, True):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test4_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo = TipoRecurso1.objects.get(nombre_recurso='Laboratorio de Electricidad')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso = 'Laboratorio de Electronica'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'Laboratorio de Electronica'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable = True
        tipo.save()
        if not self.assertEquals(tipo.reservable, True):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test5_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo = TipoRecurso1.objects.get(nombre_recurso='DROM')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso = 'DROM Helicoptero'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'DROM Helicoptero'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable = True
        tipo.save()
        if not self.assertEquals(tipo.reservable, True):
            print ('El indicador de reservable se ha modificado exitosamente')

    def test_crear_recurso(self):
        print('Prueba: Crear Recurso')
        tipo= TipoRecurso1.objects.get(nombre_recurso='Proyector')
        recurso= Recurso1.objects.create(tipo_id=tipo, estado='DI')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test1_crear_recurso(self):
        print('Prueba: Crear Recurso')
        tipo = TipoRecurso1.objects.get(nombre_recurso='Notebook')
        recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test8_crear_recurso(self):
        print('Prueba: Crear Recurso')
        tipo = TipoRecurso1.objects.get(nombre_recurso='DROM')
        recurso = Recurso1.objects.create(tipo_id=tipo, estado='DI')
        if not self.assertNotEquals(recurso, []):
            print ('El Recurso se ha creado exitosamente')

    def test8_modificar_tipo_recurso(self):
        print('Prueba: Modificar Tipo de Recurso')
        tipo = TipoRecurso1.objects.get(nombre_recurso='Laboratorio de Electricidad')
        print ('Modificar Nombre del Tipo de Recurso')
        tipo.nombre_recurso = 'Laboratorio de Informatica'
        tipo.save()
        if not self.assertEquals(tipo.nombre_recurso, 'Laboratorio de Informatica'):
            print ('El tipo de recurso se ha modificado exitosamente')
        print ('Modificar indicador de recurso reservable')
        tipo.reservable = False
        tipo.save()
        if not self.assertEquals(tipo.reservable, False):
            print ('El indicador de reservable se ha modificado exitosamente')

