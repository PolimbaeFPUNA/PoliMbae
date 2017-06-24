from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.mantenimiento.views import *
from django.contrib.auth.decorators import login_required,permission_required

urlpatterns = [

   url(r'^crear/$', permission_required('mantenimiento.add_mantenimiento')(crear_mantenimiento), name='mantenimiento_crear'),
   url(r'^crearprev/$', permission_required('mantenimiento.add_mantenimiento')(crear_mant_preventivo), name='mantenimiento_crear_prevent'),
   url(r'^listar/$', permission_required('mantenimiento.add_mantenimiento')(listar_mantenimiento), name='mantenimiento_listar'),
   url(r'^confirmar/$', permission_required('mantenimiento.add_mantenimiento')(listar_mantenimiento_confirmar), name='mantenimiento_confirmar'),
   url(r'^recuperar/$', permission_required('mantenimiento.add_mantenimiento')(listar_mantenimiento_recuperar), name='mantenimiento_recuperar'),
   url(r'^buscar/$',  permission_required('mantenimiento.add_mantenimiento')(buscar), name='mantenimiento_buscar'),
   url(r'^modificarmant/(?P<pk>\d+)$', permission_required('mantenimiento.change_mantenimiento')(modificar_mantenimiento), name="modificar_mantenimiento"),
   url(r'^eliminarmant/(?P<pk>\d+)$',permission_required('mantenimiento.change_mantenimiento')(eliminar_mantenimiento), name="eliminar_mantenimiento"),
   url(r'^entregar/(?P<id>\d+)$', permission_required('mantenimiento.change_mantenimiento')(entregar_recurso_mantenimiento), name="entregar"),
   url(r'^devolver/(?P<id>\d+)$', permission_required('mantenimiento.change_mantenimiento')(mantenimiento_recurso_devuelto), name="devolver"),
   url(r'^detalle/(?P<id>\d+)$', permission_required('mantenimiento.change_mantenimiento')(detalle_mantenimiento), name="detalle"),
]