from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.recurso.views import RecursoListar, TipoRecursoCrtaCrear, RecursoEstadoCrear, TipoRecursoModificar, \
    TipoRecursoListar,  CaracteristicaListar, CaracteristicaModificar, RecursoModificar, buscar_recurso
''' Listado de todas las urls secundarias de la url global /recurso/'''


urlpatterns = [
    url(r'^listar/$', login_required(RecursoListar.as_view()), name='recurso_listar'),
    url(r'^listartipo/$', login_required(TipoRecursoListar.as_view()), name='tiporecurso_listar'),
    url(r'^listarcaracteristica/$', login_required(CaracteristicaListar.as_view()), name='caracteristica_listar'),
    url(r'^crear/$', login_required(RecursoEstadoCrear.as_view()), name='recurso_crear'),
    url(r'^creartre/$', login_required(TipoRecursoCrtaCrear.as_view()), name='tiporecurso_crear'),
    url(r'^modificar/(?P<pk>\d+)$', login_required(TipoRecursoModificar.as_view()), name='tiporecurso_modificar'),
    url(r'^modificarctra/(?P<pk>\d+)$', login_required(CaracteristicaModificar.as_view()), name='carcteristica_modificar'),
    url(r'^modifirecurso/(?P<pk>\d+)$', login_required(RecursoModificar.as_view()), name='recurso_modificar'),
    url(r'^buscarecurso/$', login_required(buscar_recurso), name='buscar_recurso'),
]
    # Falta agregar eliminar recurso!
