from django.conf.urls import url, include
from django.contrib import admin
from app.login.views import Login, Logout
from app.usuario.views import modificar_user_admin, crear_cuenta, cambiar_password, listar_user, mod_user, crear_user,modificar_user, eliminar_user
admin.autodiscover()

''' Listado de todas las urls secundarias de Usuario, de la url global /usuarios/ del proyecto'''

# Listado de todas las urls de la aplicacion rol.

urlpatterns = [
    url(r'^crear/$', crear_user, name="crearusuario"),

   # url(r'^home/$', home, name="home"), # por el momento hay que quitar


    url(r'^(?P<iduser>[0-9]+)/eliminarusuario/$', eliminar_user, name="eliminarusuario"),
    url(r'^modificaruser/$', modificar_user, name="modificarusuario"),
    url(r'^(?P<iduser>[0-9]+)/modificaruseradmin/$', modificar_user_admin, name="modificarusuarioadmin"),
    url(r'^moduser/$', mod_user, name="moduser"),  # es una vista de bienvenida, no aparece, ver si se borra
    url(r'^listaruser/$', listar_user, name="listaruser"),

]