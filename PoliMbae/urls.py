# -*- coding: utf-8 -*-
"""PoliMbae URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app.login.views import Login, home, Logout
from app.rol.views import mod_rol
from app.usuario.views import modificar_user_admin, crear_cuenta, cambiar_password, listar_user, mod_user, crear_user,modificar_user, eliminar_user
from app.rol.views import rol_asignar
from app.recurso.views import eliminar_rec, crear_rec, mod_rec
# Urls grlobales de la aplicacion
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^rol/', include('app.rol.urls', namespace="rol")),
    url(r'^modrol/', mod_rol, name="modrol"),
    url(r'^modrecurso/', mod_rec, name="modrec"),
    url(r'^crearrec/', crear_rec, name="crearrec"),
    url(r'^eliminarrec/', eliminar_rec, name="eliminarrec"),
    url(r'^usuarios/$', crear_user, name="crearusuario"),
    url(r'^login/$', Login, name="login"),
    url(r'^logout/$', Logout, name="logout"),
    url(r'^home/$', home, name="home"),
    url(r'^(?P<iduser>[0-9]+)/eliminarusuario/$', eliminar_user, name="eliminarusuario"),
    url(r'^modificaruser/$', modificar_user, name="modificarusuario"),
    url(r'^(?P<iduser>[0-9]+)/modificaruseradmin/$', modificar_user_admin, name="modificarusuarioadmin"),
    url(r'^moduser/$', mod_user, name="moduser"),
    url(r'^listaruser/$', listar_user, name="listaruser"),
    url(r'^cuenta/$', crear_cuenta, name="cuenta"),
    url(r'^cambiarpassword/$', cambiar_password, name="cambiarpass"),

]
