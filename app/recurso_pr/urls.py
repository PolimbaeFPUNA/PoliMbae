from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.recurso_pr.views import *
from django.contrib.auth.decorators import login_required,permission_required


urlpatterns = [
    url(r'^crear/$', crear_tipo_recurso, name='recurso_pr_crear'),
    url(r'^crearrecurso/$', crear_recurso, name='recurso_pr_crear_recurso'),
    url(r'^listartipo/$', ListadoTipoRecurso.as_view(), name='recurso_pr_listar_tipo'),
    url(r'^listar/$', ListadoRecurso.as_view(), name='recurso_pr_listar'),
    url(r'^modificartipo/(?P<pk>\d+)$', TipoRecursoModificar.as_view(), name='recurso_pr_modificar'),
    url(r'^modificar/(?P<pk>\d+)$', RecursoModificar.as_view(), name='recurso_modificar'),
    url(r'^modificarcarac/(?P<ctra_id>\d+)$', modificar_caracteristicas, name='recurso_carac_modificar'),
    url(r'^listarcarac/(?P<recurso_id>\d+)$$', lista_caracteristica, name='caracteristica_listar'),
]