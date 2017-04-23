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
from app.login.views import Login, Logout
from app.rol.views import mod_rol
from app.usuario.views import modificar_user_admin, crear_cuenta, cambiar_password, listar_user, mod_user, crear_user,modificar_user, eliminar_user
from app.rol.views import rol_asignar
from app.recurso.views import eliminar_rec, crear_rec, mod_rec
# Urls grlobales de la aplicacion

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Urls Contenedoras
    url(r'^rol/', include('app.rol.urls', namespace="rol")),
    url(r'^usuarios/', include('app.usuario.urls', namespace="usuarios")),
    url(r'^recurso/', include('app.recurso.urls', namespace="recurso")),

    # Modulo de Usuarios Login/cuenta/reset pass
    url(r'^login/$', Login, name="login"),
    url(r'^logout/$', Logout, name="logout"),
    url(r'^cuenta/$', crear_cuenta, name="cuenta"),
    url(r'^cambiarpassword/$', cambiar_password, name="cambiarpass"),

    url(r'^modrol/', mod_rol, name="modrol"), # recordar eliminar
]
