from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.reserva_new.views import *
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^solicitar/', crear_solicitud, name='reserva_solicitar'),
    url(r'^listar/', solicitud_listar, name='solicitud_listar'),
    url(r'^confirmar/(?P<idsol>\d+)$', confirmar_solicitud, name='solicitud_confirmar'),
    url(r'^elimnarsol/(?P<idsol>\d+)$', eliminar_solicitud, name='eliminar_solicitud'),
    url(r'^entregar/(?P<idres>\d+)$', entregar_recurso_reserva, name='entregar_recurso'),
    url(r'^listarreserva/', listar_reserva, name='reserva_listar'),
    url(r'^listarreservauser/', listar_reserva_user, name='listar_reservas_user'),
    url(r'^devolver/(?P<idres>\d+)$', reserva_recurso_devuelto, name='devolver_recurso'),
    url(r'^cancelar/(?P<idres>\d+)$', cancelar_reserva, name='cancelar_reserva'),
    url(r'^cancelarmis/(?P<idres>\d+)$', cancelar_mi_reserva, name='cancelar_mi_reserva'),
]