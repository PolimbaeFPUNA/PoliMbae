from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.reserva_new.views import *
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [

    url(r'^solicitar/', permission_required('reserva_new.add_solicitud')(crear_solicitud), name='reserva_solicitar'),
    url(r'^listar/', permission_required('reserva_new.delete_solicitud')(solicitud_listar), name='solicitud_listar'),
    url(r'^confirmar/(?P<idsol>\d+)$', permission_required('reserva_new.delete_solicitud')(confirmar_solicitud), name='solicitud_confirmar'),
    url(r'^elimnarsol/(?P<idsol>\d+)$', permission_required('reserva_new.add_solicitud')(eliminar_solicitud), name='eliminar_solicitud'),
    url(r'^entregar/(?P<idres>\d+)$', permission_required('reserva_new.delete_reserva')(entregar_recurso_reserva), name='entregar_recurso'),
    url(r'^listarreserva/', permission_required('reserva_new.delete_reserva')(listar_reserva), name='reserva_listar'),
    url(r'^listarreservauser/', permission_required('reserva_new.add_reserva')(listar_reserva_user), name='listar_reservas_user'),
    url(r'^devolver/(?P<idres>\d+)$', permission_required('reserva_new.delete_reserva')(reserva_recurso_devuelto), name='devolver_recurso'),
    url(r'^cancelar/(?P<idres>\d+)$', permission_required('reserva_new.add_reserva')(cancelar_reserva), name='cancelar_reserva'),
    url(r'^modificar/(?P<idres>\d+)$', modificar_reserva, name='modificar_reserva'),
    url(r'^cancelarmis/(?P<idres>\d+)$', permission_required('reserva_new.add_reserva')(cancelar_mi_reserva), name='cancelar_mi_reserva'),
    url(r'^elimnarmisol/(?P<idsol>\d+)$', permission_required('reserva_new.add_solicitud')(eliminar_mi_solicitud), name='eliminar_mi_solicitud'),

]