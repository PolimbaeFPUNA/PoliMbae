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

from app.rol.views import home

from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
# Urls grlobales de la aplicacion

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Urls Contenedoras
    url(r'^rol/', include('app.rol.urls', namespace="rol")),
    url(r'^usuarios/', include('app.usuario.urls', namespace="usuarios")),
    url(r'^recurso/', include('app.recurso.urls', namespace="recurso")),
    url(r'^recurso_pr/', include('app.recurso_pr.urls', namespace="recurso_pr")),

    url(r'^reserva/', include('app.reserva.urls', namespace="reserva")),
    url(r'^mantenimiento/', include('app.mantenimiento.urls', namespace="mantenimiento")),

    # Modulo de Login

    url(r'^login/$', Login, name="login"),
    url(r'^accounts/login/', Login, name="login"),
    url(r'^logout/$', Logout, name="logout"),

    url(r'^home/', home, name="home_rol"),

    # reseteo de password

    url(r'^reset/password_reset', password_reset,
        {'template_name': 'registration/password_reset_form.html',
         'email_template_name': 'registration/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset_done', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^recpr/', include('app.recurso_pr.urls', namespace="recurso_pr")),
]
