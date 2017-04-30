from django.conf.urls import url, include
from django.contrib import admin
from app.login.views import Login, Logout
from django.contrib.auth.decorators import permission_required
from app.usuario.views import crear_user, ModificarUser, EliminarUser, ListarUser, CrearCategoria, Asignar
admin.autodiscover()

''' Listado de todas las urls secundarias de Usuario, de la url global /usuarios/ del proyecto'''

# Listado de todas las urls de la aplicacion rol.

urlpatterns = [
    url(r'^crear/$', crear_user, name="crearusuario"),
    url(r'^modificaruser/(?P<pk>\d+)$', ModificarUser.as_view(), name="modificarusuario"),
    url(r'^eliminaruser/(?P<pk>\d+)$', EliminarUser.as_view(), name="eliminarusuario"),
    url(r'^listaruser/$', ListarUser.as_view(), name="listaruser"),
    url(r'^crearcat/$', CrearCategoria.as_view(), name="crearcategoria"),
    url(r'^asignar/(?P<pk>\d+)$', permission_required('rol.modificar_user',raise_exception=True)(Asignar.as_view()), name="asignar"),
]