from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.reserva_new.views import *
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^solicitar/', crear_solicitud, name='reserva_solicitar'),
    url(r'^listar/', ListarSolicitud.as_view(), name='solicitud_listar'),
    url(r'^confirmar/(?P<idsol>\d+)$', confirmar_solicitud, name='solicitud_confirmar'),
]