from django.conf.urls import url, include
from app.reserva.views import ListarReservaGeneral, ListadoReservasAgendadas, crear_reserva, buscar,\
    borrar_reserva, reserva_modificar, ListarReservaEspecifica, ListadoReservasEspecificasAgendadas
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^listar/', ListarReservaGeneral.as_view(), name='reserva_listar'),
    url(r'^listaragenda/$', ListadoReservasAgendadas.as_view(), name='agenda_listar'),
    url(r'^crear/(?P<recurso_id>\d+)$', crear_reserva, name='crear_reserva'),
    url(r'^buscar/$', buscar, name='buscar_recurso'),
    url(r'^eliminar/(?P<reserva_id>\d+)$', borrar_reserva, name='eliminar_reserva'),
    url(r'^modificar/(?P<reserva_id>\d+)$', reserva_modificar, name='reserva_modificar'),
    url(r'^listaespecifica/', ListarReservaEspecifica.as_view(), name='reserva_especifica_listar'),
    url(r'^agendaespecifica/', ListadoReservasEspecificasAgendadas.as_view(), name='agenda_especifica_listar'),
    ]
