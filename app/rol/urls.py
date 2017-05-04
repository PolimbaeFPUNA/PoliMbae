from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required,permission_required
from app.rol.views import rol_crear, home,  \
    ListarRol, rol_asignar, PermisoListar, PermisoRolCrear, CrearPermiso, ModificarRol, ModificarPermiso, EliminarRol, \
    EliminarPermiso, permisoCr, rol_listar, ModificarRolG,ListarPermiso

admin.autodiscover()
''' Listado de todas las urls secundarias de la url global /rol/'''

# Listado de todas las urls de la aplicacion rol.
urlpatterns = [
    url(r'^crear/$', permission_required('rol.crear_rol','/login/')(rol_crear), name='rol_crear'),
    url(r'^listarrol/$', login_required(rol_listar), name='rol_listar'),
    url(r'^listar/$', login_required(ListarRol.as_view()), name='rol_listar'),
    url(r'^listarpermiso/$', login_required(ListarPermiso.as_view()), name='permiso_listar'),
    url(r'^modificar/(?P<pk>\d+)$', login_required(ModificarRol.as_view()), name='modificar_rol'),
    url(r'^modificarg/(?P<pk>\d+)$', login_required(ModificarRolG.as_view()), name='modificar'),
    url(r'^modificarpermiso/(?P<pk>\d+)$', login_required(ModificarPermiso.as_view()), name='modificar_permiso'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(EliminarRol.as_view()), name='eliminar_rol'),
    url(r'^eliminarpermiso/(?P<pk>\d+)$', login_required(EliminarPermiso.as_view()), name='eliminar_permiso'),
    url(r'^crearpermisorol/$', login_required(PermisoRolCrear.as_view()), name='permiso_rol_crear'),
    url(r'^crearpermiso/$', login_required(CrearPermiso.as_view()), name='permiso_crear'),
    url(r'^asignar/$', login_required(rol_asignar), name='rol_asignar'),
    url(r'^home/$', login_required(home), name='home'),
    url(r'^permiso/$',login_required(permisoCr),name='permiso'),
]
