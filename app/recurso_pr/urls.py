from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.recurso_pr.views import *
from django.contrib.auth.decorators import login_required,permission_required



'''Urls del modulo de Recursos para Crear Tipo de Recurso, Recurso y Caracteristicas,
ademas de listarlos y modificarlos '''

urlpatterns = [
    url(r'^crear/$', permission_required('recurso_pr.add_tiporecurso1')(crear_tipo_recurso), name='recurso_pr_crear'),
    url(r'^crearrecurso/$', permission_required('recurso_pr.add_recurso1')(crear_recurso), name='recurso_pr_crear_recurso'),
    url(r'^listartipo/$', permission_required('recurso_pr.add_tiporecurso1')(ListadoTipoRecurso.as_view()), name='recurso_pr_listar_tipo'),
    url(r'^listar/$', permission_required('recurso_pr.add_recurso1')(ListadoRecurso.as_view()), name='recurso_pr_listar'),
    url(r'^modificartipo/(?P<pk>\d+)$', permission_required('recurso_pr.chage_tiporecurso1')(TipoRecursoModificar.as_view()), name='recurso_pr_modificar'),
    url(r'^modificar/(?P<recurso_id>\d+)$', permission_required('recurso_pr.chage_recurso1')(recurso_edit), name='recurso_modificar'),
    url(r'^modificarcarac/(?P<ctra_id>\d+)$', permission_required('recurso_pr.chage_recurso1')(modificar_caracteristicas), name='recurso_carac_modificar'),
    url(r'^listarcarac/(?P<recurso_id>\d+)$$', permission_required('recurso_pr.chage_recurso1')(lista_caracteristica), name='caracteristica_listar'),

]