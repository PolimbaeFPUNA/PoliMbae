from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.decorators import login_required,permission_required
from app.rol.views import rol_crear, home,  \
    ListarRol, rol_asignar, PermisoListar, PermisoRolCrear, CrearPermiso, ModificarRol, ModificarPermiso, EliminarRol, \
    EliminarPermiso, permisoCr, rol_listar, ModificarRolG,ListarPermiso

from django.contrib.auth.decorators import login_required
from app.rol.views import rol_crear, home, \
    ListarRol, rol_asignar, PermisoListar, PermisoRolCrear, CrearPermiso, ModificarRol, ModificarPermiso, EliminarRol, \
    EliminarPermiso


admin.autodiscover()
''' Listado de todas las urls secundarias de la url global /rol/'''

# Listado de todas las urls de la aplicacion rol.
urlpatterns = [

    url(r'^crear/$', permission_required('rol.add_userrol','/login/')(rol_crear), name='rol_crear'),
    url(r'^listarrol/$', permission_required('rol.change_userrol', '/login/')(rol_listar), name='rol_listar'),
    url(r'^listar/$', permission_required('rol.change_userrol','/login/')(ListarRol.as_view()), name='rol_listar'),
    url(r'^listarpermiso/$', permission_required('rol.change_permisorol','/login/')(ListarPermiso.as_view()), name='permiso_listar'),
    url(r'^modificar/(?P<pk>\d+)$', permission_required('rol.change_userrol', '/login/')(ModificarRol.as_view()), name='modificar_rol'),
    url(r'^modificarg/(?P<pk>\d+)$', permission_required('rol.change_userrol')(ModificarRolG.as_view()), name='modificar'),
    url(r'^modificarpermiso/(?P<pk>\d+)$', permission_required('rol.change_permisorol')(ModificarPermiso.as_view()), name='modificar_permiso'),
    url(r'^eliminar/(?P<pk>\d+)$', permission_required('rol.delete_permisorol')(EliminarRol.as_view()), name='eliminar_rol'),
    url(r'^eliminarpermiso/(?P<pk>\d+)$', permission_required('rol.delete_permisorol')(EliminarPermiso.as_view()), name='eliminar_permiso'),
    url(r'^crearpermisorol/$', permission_required('rol.add_permisorol')(PermisoRolCrear.as_view()), name='permiso_rol_crear'),
    url(r'^crearpermiso/$', permission_required('rol.add_permisorol')(CrearPermiso.as_view()), name='permiso_crear'),
    url(r'^asignar/$', permission_required('rol.add_userrol')(rol_asignar), name='rol_asignar'),
    url(r'^home/$', login_required(home), name='home'),

    url(r'^permiso/$',permission_required('rol.add_permisorol')(permisoCr),name='permiso'),


]
