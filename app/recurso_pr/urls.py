from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.recurso_pr.views import *
from django.contrib.auth.decorators import login_required,permission_required



'''Urls del modulo de Recursos para Crear Tipo de Recurso, Recurso y Caracteristicas,
ademas de listarlos y modificarlos '''

urlpatterns = [
    url(r'^crear/$', login_required(crear_tipo_recurso), name='recurso_pr_crear'),
    url(r'^crearrecurso/$', login_required(crear_recurso), name='recurso_pr_crear_recurso'),
    url(r'^listartipo/$', login_required(ListadoTipoRecurso.as_view()), name='recurso_pr_listar_tipo'),
    url(r'^listar/$', login_required(ListadoRecurso.as_view()), name='recurso_pr_listar'),
    url(r'^modificartipo/(?P<pk>\d+)$', login_required(TipoRecursoModificar.as_view()), name='recurso_pr_modificar'),
    url(r'^modificar/(?P<recurso_id>\d+)$', login_required(recurso_edit), name='recurso_modificar'),
    url(r'^modificarcarac/(?P<ctra_id>\d+)$', login_required(modificar_caracteristicas), name='recurso_carac_modificar'),
    url(r'^listarcarac/(?P<recurso_id>\d+)$$', login_required(lista_caracteristica), name='caracteristica_listar'),

]