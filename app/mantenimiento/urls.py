from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.mantenimiento.views import *

urlpatterns = [

   url(r'^crear/$', login_required(crear_mantenimiento), name='mantenimiento_crear'),
   url(r'^listar/$', login_required(listar_mantenimiento), name='mantenimiento_listar'),
   url(r'^buscar/$',  login_required(buscar), name='mantenimiento_buscar'),
   url(r'^modificarmant/(?P<pk>\d+)$', login_required(modificar_mantenimiento), name="modificar_mantenimiento"),
   url(r'^eliminaruser/(?P<pk>\d+)$', login_required(EliminarMant.as_view()), name="eliminar_mantenimiento"),
]