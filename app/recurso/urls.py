from django.conf.urls import url, include

from app.recurso.views import RecursoListar, TipoRecursoCrtaCrear, RecursoEstadoCrear, TipoRecursoModificar, \
    TipoRecursoListar,  CaracteristicaListar, CaracteristicaModificar, RecursoModificar
''' Listado de todas las urls secundarias de la url global /recurso/'''


urlpatterns = [
    url(r'^listar/$', RecursoListar.as_view(), name='recurso_listar'),
    url(r'^listartipo/$', TipoRecursoListar.as_view(), name='tiporecurso_listar'),
    url(r'^listarcaracteristica/$', CaracteristicaListar.as_view(), name='caracteristica_listar'),
    url(r'^crear/$', RecursoEstadoCrear.as_view(), name='recurso_crear'),
    url(r'^creartre/$', TipoRecursoCrtaCrear.as_view(), name='tiporecurso_crear'),
    url(r'^modificar/(?P<pk>\d+)$', TipoRecursoModificar.as_view(), name='tiporecurso_modificar'),
    url(r'^modificarctra/(?P<pk>\d+)$', CaracteristicaModificar.as_view(), name='carcteristica_modificar'),
    url(r'^modifirecurso/(?P<pk>\d+)$', RecursoModificar.as_view(), name='recurso_modificar'),
]
    # Falta agregar eliminar recurso!
