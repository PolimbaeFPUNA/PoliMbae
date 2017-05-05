from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.recurso.views import RecursoListar, TipoRecursoCrtaCrear, RecursoEstadoCrear, TipoRecursoModificar, \
    TipoRecursoListar,  CaracteristicaListar, CaracteristicaModificar, RecursoModificar, buscar_recurso
''' Listado de todas las urls secundarias de la url global /recurso/'''


urlpatterns = [
    url(r'^listar/$', permission_required('recurso.change_recurso1')(RecursoListar.as_view()), name='recurso_listar'),
    url(r'^listartipo/$', permission_required('recurso.change_recurso1')(TipoRecursoListar.as_view()), name='tiporecurso_listar'),
    url(r'^listarcaracteristica/$', permission_required('recurso.change_recurso1')(CaracteristicaListar.as_view()), name='caracteristica_listar'),
    url(r'^crear/$', permission_required('recurso.add_recurso1')(RecursoEstadoCrear.as_view()), name='recurso_crear'),
    url(r'^creartre/$', permission_required('recurso.add_recurso1')(TipoRecursoCrtaCrear.as_view()), name='tiporecurso_crear'),
    url(r'^modificar/(?P<pk>\d+)$', permission_required('recurso.change_recurso1')(TipoRecursoModificar.as_view()), name='tiporecurso_modificar'),
    url(r'^modificarctra/(?P<pk>\d+)$', permission_required('recurso.change_recurso1')(CaracteristicaModificar.as_view()), name='carcteristica_modificar'),
    url(r'^modifirecurso/(?P<pk>\d+)$', permission_required('recurso.change_recurso1')(RecursoModificar.as_view()), name='recurso_modificar'),
    url(r'^buscarecurso/$', permission_required('rol.buscar_recurso')(buscar_recurso), name='buscar_recurso'),
]
    # Falta agregar eliminar recurso!
