from django.test import TestCase
from app.recurso.models import *
from datetime import date
# Create your tests here.


class RecursoTestCase(TestCase):
    print ('\nTests para Recurso ')

    def setUp(self):

        caracteristica= Caracteristica.objects.create(nombre_caracteristica='marca', activo=True)
        tipo= TipoRecurso1.objects.create(nombre_recurso='Proyector', reservable= True, fecha_mantenimiento='2017-05-02', ctra_id= caracteristica)
        Recurso1.objects.create(tipo_id=tipo, estado='DI')

    def test_crear_tipo_recurso(self):

        print('Prueba: Crear Tipo de Recurso')
        caracteristica= Caracteristica.objects.get(nombre_caracteristica='marca')
        tipo= TipoRecurso1.objects.create(nombre_recurso='Notebook', reservable=True, fecha_mantenimiento='2017-05-02', ctra_id=caracteristica)

        if not self.assertNotEquals(tipo, []):
            print ('El Tipo de recurso se ha creado exitosamente')
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
        print('Modificar la fecha de mantenimiento preventivo')
        tipo.fecha_mantenimiento= date.today()
        tipo.save()
        if not self.assertEquals(tipo.fecha_mantenimiento,date.today()):
            print('La fecha del mantenimiento preventivo se ha modificado')

    def test_crear_recurso(self):
        print('Prueba: Crear Recurso')
        tipo= TipoRecurso1.objects.get(nombre_recurso='Proyector')
        recurso= Recurso1.objects.create(tipo_id=tipo, estado='DI')
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