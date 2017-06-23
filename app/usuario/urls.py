from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required,permission_required
from app.login.views import Login, Logout

from django.contrib.auth.decorators import permission_required
from app.usuario.views import *

admin.autodiscover()

''' Listado de todas las urls secundarias de Usuario, de la url global /usuarios/ del proyecto'''

# Listado de todas las urls de la aplicacion rol.

urlpatterns = [

    url(r'^crear/$', permission_required('usuario.delete_profile')(UsuarioCreate.as_view()), name="crear_usuario"),
    url(r'^modificaruser/(?P<pk>\d+)$', permission_required('usuario.change_profile')(ModificarUser.as_view()), name="modificarusuario"),
    url(r'^eliminaruser/(?P<pk>\d+)$', permission_required('usuario.delete_profile')(EliminarUser.as_view()), name="eliminarusuario"),
    url(r'^listaruser/$', permission_required('usuario.change_profile')(ListarUser.as_view()), name="listaruser"),

    #url(r'^asignar/(?P<pk>\d+)$', permission_required('rol.change_userrol')(Asignar.as_view()), name="asignar"),

    url(r'^crearcuenta/$', register_user, name="registrar_usuario"),
    url(r'^activar/(?P<user>\w+)/', permission_required('usuario.delete_profile')(activar_cuenta), name="activar"),
    url(r'^desactivar/(?P<user>\w+)/',permission_required('usuario.delete_profile')(desactivar_user), name="desactivar"),
    url(r'^listarprofile/$', permission_required('usuario.delete_profile')(ListaUserProfile.as_view()), name="listaprofile"),
    url(r'^confirm/(?P<activation_key>\w+)/', permission_required('usuario.delete_profile')(confirmar), name="confirmar"),
    url(r'^asignarcategoria/(?P<user>\w+)/', permission_required('usuario.delete_profile')(asignar_categoria), name="asignar_categoria"),
    url(r'^asignar/(?P<pk>\d+)$', asignar_group , name="asignar"),

]