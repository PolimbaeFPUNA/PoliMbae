from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.mantenimiento.views import *
from django.contrib.auth.decorators import login_required,permission_required

urlpatterns = [

   url(r'^crear/$', permission_required('mantenimiento.add_mantenimiento','/login/')(crear_mantenimiento), name='mantenimiento_crear'),
   url(r'^listar/$', permission_required('mantenimiento.change_mantenimiento','/login/')(listar_mantenimiento), name='mantenimiento_listar'),
   url(r'^buscar/$',  login_required(buscar), name='mantenimiento_buscar'),
   url(r'^modificarmant/(?P<pk>\d+)$', permission_required('mantenimiento.change_mantenimiento')(modificar_mantenimiento), name="modificar_mantenimiento"),
   url(r'^eliminaruser/(?P<pk>\d+)$', permission_required('mantenimiento.delete_mantenimiento')(EliminarMant.as_view()), name="eliminar_mantenimiento"),
]