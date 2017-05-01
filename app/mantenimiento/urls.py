from django.conf.urls import url, include
from app.mantenimiento.views import *

urlpatterns = [

   url(r'^crear/$', crear_mantenimiento, name='mantenimiento_crear'),
   url(r'^listar/$', listar_mantenimiento, name='mantenimiento_listar'),
   url(r'^modificarmant/(?P<pk>\d+)$', modificar_mantenimiento, name="modificar_mantenimiento"),
   url(r'^eliminaruser/(?P<pk>\d+)$', EliminarMant.as_view(), name="eliminar_mantenimiento"),
]