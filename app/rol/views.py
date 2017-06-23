
from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from app.log.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from app.usuario.models import Profile
from app.rol.models import UserRol, PermisoRol
from app.rol.forms import AsignarRolForm, RolForm, PermisoForm, PermisoForm2,RolGrupo,PermisoGrupo
from django.contrib.auth.models import Group, Permission,ContentType
from django.contrib.auth.decorators import permission_required, login_required
from datetime import datetime,timedelta, date
# Create your views here.

''' Funciones referentes al Rol, crear, modificar, eliminar, listar, asignar y desasignar rol a un usuario'''

@login_required
def home(request):

    return render(request,'rol/home_rol.html')

@login_required
def rol_crear(request):
    """Si se reciben datos sera el metodo Post, por lo que se guardara el nuevo registro de rol
        crear_form: es la variable donde se guardan los datos enviados por el cliente a traves del formulario.
        RolForm: es el formulario en donde se cargan los datos en el template crear_rol.html
        crear_rol.html: es el template donde se crea el nuevo rol
        rol_listar.html: es el template donde se redirecciona, despues de concretarse una accion.
    """
    if request.method == 'POST':
        crear_form = RolGrupo(request.POST)

        # se validan los datos recibidos del post en la variable
        if crear_form.is_valid():

            rol=crear_form.save()  # se guardan los datos del formulario

            Log.objects.create(usuario=request.user,fecha_hora=datetime.now(),mensaje='Crear rol '+rol.__str__())
        return redirect('rol:rol_listar')
    else:
        crear_form = RolGrupo()
    # se coloca el nombre del template y el archivo de html donde esta el formulario y el contexto del formulario
    return render(request, 'rol/crear_rol.html', {'crear_form': crear_form})


# vista basada en funciones
@login_required
def rol_listar(request):
    """ Funcion que Lista todos los registros creados del modelo Rolusuario y los envia al template listar_rol.html"""

    qroles = RolGrupo.objects.all().order_by('id')

    contexto = {'roles': qroles}
    return render(request, 'rol/listar_rol.html', contexto)


# vista basada en clases

class ListarRol (ListView):
    """Clase para crear el Listado de los roles, se indica el modelo y el template que lo contendra"""
    # Se indica el modelo Rolusuario

    model = Group

    template_name = 'rol/listar_rol.html'
    paginate_by = 10

class EliminarRol(DeleteView):

    model = Group
    form_class = RolGrupo
    template_name = 'rol/eliminar_rol.html'
    success_url = reverse_lazy('rol:rol_listar')


class EliminarPermiso(DeleteView):
    model = Permission
    form_class = PermisoGrupo

    template_name = 'rol/eliminar_permiso.html'
    success_url = reverse_lazy('rol:permiso_listar')

''' Modificar Rol y Permisos'''


class ModificarRol(UpdateView):
    model = UserRol
    form_class = UserRol
    template_name = 'rol/modificar.html'
    success_url = reverse_lazy('rol:rol_listar')


class ModificarRolG (UpdateView):
    model= Group
    template_name = 'rol/modificar.html'
    form_class = RolGrupo
    success_url = reverse_lazy('rol:rol_listar')
    def get_context_data(self, **kwargs):
        context = super(ModificarRolG, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        rol= self.model.objects.get(id=pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_usuario = kwargs['pk']
        usuario = self.model.objects.get(id=id_usuario)
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid(): #and form2.is_valid():
            form.save()
            #form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class ModificarPermiso(UpdateView):
    model = Permission
    form_class = PermisoGrupo
    template_name = 'rol/modificar_permiso.html'
    success_url = reverse_lazy('rol:permiso_listar')
    def get_context_data(self, **kwargs):
        context = super(ModificarPermiso, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        per = self.model.objects.get(id=pk)
        if 'form' not in context:
            context['form'] = self.form_class()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object

        id_usuario = kwargs['pk']
        usuario = self.model.objects.get(id=id_usuario)
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():  # and form2.is_valid():
            form.save()
            # form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())




''' Funciones y Clases de permisos y roles '''

@login_required
def permiso_listar(request):
    """ Funcion que Lista todos los registros creados del modelo Rolusuario y los envia al template listar_rol.html"""
    qpermiso = Permission.objects.all().order_by('id')
    contexto = {'permiso': qpermiso}
    return render(request, 'rol/listar_permisos.html', contexto)

''' Esta clase crea un permiso a un rol existente'''
class ListarPermiso (ListView):
    """Clase para crear el Listado de los roles, se indica el modelo y el template que lo contendra"""
    # Se indica el modelo Rolusuario
    model = Permission
    template_name = 'rol/listar_permisos.html'
    paginate_by = 10

class CrearPermiso(CreateView):
    model = PermisoRol
    form_class = PermisoForm
    template_name = 'rol/asignar_permiso.html'
    success_url = reverse_lazy('rol:permiso_listar')


class PermisoListar(ListView):
    model = PermisoRol
    template_name = 'rol/listar_permisos.html'

''' Crea un permiso y tambien un registro de Rol'''


class PermisoModificar(UpdateView):
    model = Permission
    form_class = PermisoGrupo
    template_name = 'rol/modificar_permiso.html'
    success_url = reverse_lazy('rol:permiso_listar')



class PermisoRolCrear(CreateView):
    model = PermisoRol
    template_name = 'rol/crear_rol_permiso.html'
    form_class = PermisoForm2
    second_form_class = RolForm
    success_url = reverse_lazy('rol:permiso_listar')

    def get_context_data(self, **kwargs):
        context = super(PermisoRolCrear, self).get_context_data(**kwargs)
        if 'form_permiso' not in context:
            context['form_permiso'] = self.form_class(self.request.GET)
        if 'form_rol' not in context:
            context['form_rol'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form_permiso = self.form_class(request.POST)
        form_rol = self.second_form_class(request.POST)
        if form_permiso.is_valid() and form_rol.is_valid():
            permisorol = form_permiso.save(commit=False)
            permisorol.rol_id = form_rol.save()
            permisorol.save()
            return HttpResponseRedirect(self.get_success_url())
        else:

            return self.render_to_response(self.get_context_data(form=form_permiso, form2=form_rol))



@login_required
def mod_rol(request):
    return render(request, 'rol/../login/home.html')




@login_required
def rol_asignar(request):
    mensaje = None
    if request.method == 'POST':
        cedula = request.POST['cedula']
        nuevo_rol = request.POST['rol']
        if Profile.objects.filter(cedula=cedula):
            user = Profile.objects.get(cedula=cedula)
            user.rol = nuevo_rol
            user.save()
            mensaje = "Rol Asignado"
        else:
            mensaje = "No es un Usuario valido"
        formS = AsignarRolForm
        context = {
            'mensaje':mensaje,
            'formS':formS,
        }
        return render(request,'rol/asignar_rol.html',context)
    else:
        formS = AsignarRolForm
        context = {
            'mensaje': mensaje,
            'formS': formS,
        }
    return render(request, 'rol/asignar_rol.html', context)


@login_required
def permisoCr(request):
    """Si se reciben datos sera el metodo Post, por lo que se guardara el nuevo registro de rol
        crear_form: es la variable donde se guardan los datos enviados por el cliente a traves del formulario.
        RolForm: es el formulario en donde se cargan los datos en el template crear_rol.html
        crear_rol.html: es el template donde se crea el nuevo rol
        rol_listar.html: es el template donde se redirecciona, despues de concretarse una accion.
    """
    if request.method == 'POST':
        crear_form = PermisoGrupo(request.POST)
        # se validan los datos recibidos del post en la variable
        if crear_form.is_valid():
            cod=request.POST['codename']
            nam=request.POST['name']
            cont=ContentType.objects.get_for_model(UserRol)
            p=Permission.objects.get_or_create(codename=cod,name=nam,content_type=cont)
             # se guardan los datos del formulario
        return redirect('rol:permiso_listar')
    else:
        crear_form = PermisoGrupo()
    # se coloca el nombre del template y el archivo de html donde esta el formulario y el contexto del formulario
    return render(request, 'rol/asignar_permiso.html', {'crear_form': crear_form})
