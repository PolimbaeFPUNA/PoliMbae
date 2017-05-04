from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from app.login.views import Login, Logout
from app.usuario.views import crear_user, ModificarUser, EliminarUser, ListarUser, CrearCategoria
from django.contrib.auth.decorators import permission_required
admin.autodiscover()

''' Listado de todas las urls secundarias de Usuario, de la url global /usuarios/ del proyecto'''

# Listado de todas las urls de la aplicacion rol.

urlpatterns = [
    url(r'^crear/$', login_required(crear_user), name="crearusuario"),
    url(r'^modificaruser/(?P<pk>\d+)$',  login_required(ModificarUser.as_view()), name="modificarusuario"),
    url(r'^eliminaruser/(?P<pk>\d+)$',  login_required(EliminarUser.as_view()), name="eliminarusuario"),
    url(r'^listaruser/$',  login_required(ListarUser.as_view()), name="listaruser"),
    url(r'^crearcat/$',  login_required(CrearCategoria.as_view()), name="crearcategoria"),
]