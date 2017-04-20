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
from django.conf.urls import url
from django.contrib import admin
from app.usuario.views import registrar_user
from app.usuario.views import eliminar_user
from app.usuario.views import modificar_user
from app.login.views import Login
from app.login.views import home
from app.login.views import Logout
from app.usuario.views import mod_user
from app.usuario.views import listar_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^usuarios/$', registrar_user, name="crearusuario"),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout, name="logout"),
    url(r'^home/$', home, name="home"),
    url(r'^(?P<iduser>[0-9]+)/eliminarusuario/$', eliminar_user, name="eliminarusuario"),
    url(r'^modificaruser/$', modificar_user, name="modificarusuario"),
    url(r'^moduser/$', mod_user, name="moduser"),
    url(r'^listaruser/$', listar_user, name="listaruser"),
]
