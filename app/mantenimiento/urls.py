from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.mantenimiento.views import *
from django.contrib.auth.decorators import login_required,permission_required

urlpatterns = [

   url(r'^crear/$', crear_mantenimiento, name='mantenimiento_crear'),
   url(r'^crearprev/$', crear_mant_preventivo, name='mantenimiento_crear_prevent'),
   url(r'^listar/$', listar_mantenimiento, name='mantenimiento_listar'),
   url(r'^confirmar/$', listar_mantenimiento_confirmar, name='mantenimiento_confirmar'),
   url(r'^recuperar/$', listar_mantenimiento_recuperar, name='mantenimiento_recuperar'),
   url(r'^buscar/$',  buscar, name='mantenimiento_buscar'),
   url(r'^modificarmant/(?P<pk>\d+)$', modificar_mantenimiento, name="modificar_mantenimiento"),
   url(r'^eliminarmant/(?P<pk>\d+)$',eliminar_mantenimiento, name="eliminar_mantenimiento"),
]