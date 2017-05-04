from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.reserva.views import ListarReservaGeneral, ListadoReservasAgendadas, crear_reserva, buscar,\
    borrar_reserva, reserva_modificar, ListarReservaEspecifica, ListadoReservasEspecificasAgendadas
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^listar/',  login_required(ListarReservaGeneral.as_view()), name='reserva_listar'),
    url(r'^listaragenda/$',  login_required(ListadoReservasAgendadas.as_view()), name='agenda_listar'),
    url(r'^crear/(?P<recurso_id>\d+)$',  login_required(crear_reserva), name='crear_reserva'),
    url(r'^buscar/$',  login_required(buscar), name='buscar_recurso'),
    url(r'^eliminar/(?P<reserva_id>\d+)$',  login_required(borrar_reserva), name='eliminar_reserva'),
    url(r'^modificar/(?P<reserva_id>\d+)$',  login_required(reserva_modificar), name='reserva_modificar'),
    url(r'^listaespecifica/',  login_required(ListarReservaEspecifica.as_view()), name='reserva_especifica_listar'),
    url(r'^agendaespecifica/',  login_required(ListadoReservasEspecificasAgendadas.as_view()), name='agenda_especifica_listar'),
    ]
