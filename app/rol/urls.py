from django.conf.urls import url, include
from django.contrib import admin
from app.rol.views import rol_crear, modificar_rol, eliminar_rol, \
    ListarRol, rol_asignar

admin.autodiscover()
''' Listado de todas las urls secundarias de la url global /rol/'''

# Listado de todas las urls de la aplicacion rol.
urlpatterns = [
    url(r'^crear/$', rol_crear, name='rol_crear'),
    url(r'^listar/$', ListarRol.as_view(), name='rol_listar'),
    url(r'^modificar/(?P<id_rol>\d+)/$', modificar_rol, name='rol_modificar'),
    url(r'^eliminar/(?P<id_rol>\d+)/$', eliminar_rol, name='rol_eliminar'),
    url(r'^asignar/$', rol_asignar, name='rol_asignar'),
]
