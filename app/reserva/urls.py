from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.reserva.views import ListarReservaGeneral, ListadoReservasAgendadas, crear_reserva, buscar,\
    borrar_reserva, reserva_modificar, ListarReservaEspecifica, ListadoReservasEspecificasAgendadas, buscar_especifica, \
    crear_reserva_especifica, pila_prioridades
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [
    url(r'^listar/', ListarReservaGeneral.as_view(), name='reserva_listar'),
    url(r'^listaragenda/$',  permission_required('reserva.change_listareservageneral')(ListadoReservasAgendadas.as_view()), name='agenda_listar'),
    url(r'^crear/(?P<recurso_id>\d+)$', crear_reserva, name='crear_reserva'),
    url(r'^buscar/$',  login_required(buscar), name='buscar_recurso'),
    url(r'^eliminar/(?P<reserva_id>\d+)$',  permission_required('reserva.delete_reservageneral')(borrar_reserva), name='eliminar_reserva'),
    url(r'^modificar/(?P<reserva_id>\d+)$',  permission_required('reserva.change_reservageneral')(reserva_modificar), name='reserva_modificar'),
    url(r'^listaespecifica/',  login_required(ListarReservaEspecifica.as_view()), name='reserva_especifica_listar'),
    url(r'^agendaespecifica/',  login_required(ListadoReservasEspecificasAgendadas.as_view()), name='agenda_especifica_listar'),
    url(r'^modificar2/(?P<reserva_id>\d+)$', reserva_modificar, name='reserva_modificar2'),
    url(r'^buscarespecifica/$',  login_required(buscar_especifica), name='buscar_recurso_especifico'),
    url(r'^crearespecifica/(?P<recurso_id>\d+)$', crear_reserva_especifica, name='crear_reserva_especifica'),
    url(r'^listarprioridad/', pila_prioridades, name='pila'),
    ]
