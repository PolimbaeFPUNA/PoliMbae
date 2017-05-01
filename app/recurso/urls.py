from django.conf.urls import url, include
from django.contrib import admin
from app.login.views import Login, Logout
from app.rol.views import rol_asignar
from app.recurso.views import eliminar_rec, crear_rec, mod_rec

urlpatterns = [
    url(r'^modrecurso/', mod_rec, name="modrec"),  # no poner aca
    url(r'^crearrec/', crear_rec, name="crearrec"),  # no poner aca
    url(r'^eliminarrec/', eliminar_rec, name="eliminarrec"),  # no poner aca
]