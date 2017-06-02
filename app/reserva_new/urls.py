from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.reserva_new.views import *
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^solicitar/', crear_solicitud, name='reserva_solicitar'),
    url(r'^listar/', solicitud_listar, name='solicitud_listar'),
    url(r'^confirmar/(?P<idsol>\d+)$', confirmar_solicitud, name='solicitud_confirmar'),
    url(r'^entregar/(?P<idres>\d+)$', entregar_recurso_reserva, name='entregar_recurso'),
    url(r'^listarreserva/', listar_reserva, name='reserva_listar'),
    url(r'^listarreservauser/', listar_reserva_user, name='listar_reservas_user'),
]