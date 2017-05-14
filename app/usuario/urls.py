from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required,permission_required
from app.login.views import Login, Logout

from django.contrib.auth.decorators import permission_required
from app.usuario.views import crear_user, ModificarUser, EliminarUser, ListarUser, CrearCategoria, Asignar

admin.autodiscover()

''' Listado de todas las urls secundarias de Usuario, de la url global /usuarios/ del proyecto'''

# Listado de todas las urls de la aplicacion rol.

urlpatterns = [

    url(r'^crear/$', permission_required('usuario.add_profile')(crear_user), name="crearusuario"),
    url(r'^modificaruser/(?P<pk>\d+)$', permission_required('usuario.change_profile')(ModificarUser.as_view()), name="modificarusuario"),
    url(r'^eliminaruser/(?P<pk>\d+)$', permission_required('usuario.delete_profile')(EliminarUser.as_view()), name="eliminarusuario"),
    url(r'^listaruser/$', ListarUser.as_view(), name="listaruser"),
    url(r'^crearcat/$', permission_required('usuario.add_profile')(CrearCategoria.as_view()), name="crearcategoria"),
    url(r'^asignar/(?P<pk>\d+)$', permission_required('rol.change_userrol')(Asignar.as_view()), name="asignar"),



]