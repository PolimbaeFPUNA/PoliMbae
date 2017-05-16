
from django.shortcuts import render, redirect

from django.http import  HttpResponseRedirect
from app.rol.forms import RolForm

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from app.usuario.models import Profile
from app.rol.models import UserRol, PermisoRol
from app.reserva.models import *
from app.reserva.views import *
import datetime
from datetime import date, timedelta
import string
from app.rol.forms import AsignarRolForm, RolForm, PermisoForm, PermisoForm2,RolGrupo,PermisoGrupo
from django.contrib.auth.models import Group, Permission,ContentType


# Create your views here.

''' Funciones referentes al Rol, crear, modificar, eliminar, listar, asignar y desasignar rol a un usuario'''


def home(request):
    ver_reservas_especifcas()
    return render_to_response('rol/home_rol.html')


def ver_prioridad(usuario):
    reserva = ReservaEspecifica.objects.all()
    for p in reserva:
        if p.profile.cedula == usuario:
            cate = p.profile.categoria
            if cate == 'Institucional':
                prioridad = 1
                return prioridad
            if cate == 'Titular':
                prioridad = 2
                return prioridad
            if cate == 'Adjunto':
                prioridad = 3
                return prioridad
            if cate == 'Asistente':
                prioridad = 4
                return prioridad
            if cate == 'Encargado de Catedra':
                prioridad = 5
                return prioridad
            if cate == 'Auxiliar de Ensenanza':
                prioridad = 6
                return prioridad
            if cate == 'Alumno':
                prioridad = 7
                return prioridad
            if cate == 'Funcionario':
                prioridad = 8
                return prioridad


def verificar_hora_reserva_especifica(usuario, fecha_reserva, hora_inicio, hora_fin, recurso, prioridad):
    """Funcion que controla que  el recurso no este reservado para la fecha y hora de inicio existentes
    retorna 1 si se encuentra la colision"""
    especifica = ListaReservaEspecifica.objects.all()  # Retorana todos los objetos de la tabla
    nro = int(recurso)
    for p in especifica:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        priori = ver_prioridad(p.usuario)
        if p.usuario != usuario:
            if p.recurso_reservado == nro:
                if p.fecha_reserva == fecha_reserva:
                    if hora1 == hora_inicio:
                        if priori <= prioridad:
                            return 1
    return 0


def verificar_horainicio_intermedia_especifica(usuario, fecha_reserva, hora_inicio, hora_fin, recurso, prioridad):
    """ Funcion que controla que en la fecha de reserva indicaca, no se tenga la
    hora de inicio de reserva en forma intermedia en otro horario ya reservado"""
    especifica = ListaReservaEspecifica.objects.all()  # Retorana todos los objetos de la tabla
    nro = int(recurso)
    for p in especifica:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        priori = ver_prioridad(p.usuario)
        if p.usuario != usuario:
            if p.recurso_reservado == nro:
                if p.fecha_reserva == fecha_reserva:
                    if hora_inicio > hora1:
                        if hora_inicio < hora2:
                            if priori <= prioridad:
                                return 1
    return 0


def verificar_horafin_intermedia_especifica(usuario, fecha_reserva, hora_inicio, hora_fin, recurso, prioridad):
    """ Funcion que controla que en la fecha de reserva indicaca, no se tenga la
       hora de finalizacion de reserva en forma intermedia en otro horario ya reservado"""
    especifica = ListaReservaEspecifica.objects.all()  # Retorana todos los objetos de la tabla
    nro = int(recurso)
    for p in especifica:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        priori = ver_prioridad(p.usuario)
        if p.usuario != usuario:
            if p.recurso_reservado == nro:
                if p.fecha_reserva == fecha_reserva:
                    if hora_fin > hora2:
                        if hora_fin < hora2:
                            if priori <= prioridad:
                                return 1
    return 0


def enviar_mensaje(r):
    reserva_especifica = ReservaEspecifica.objects.all()
    for p in reserva_especifica:
        if p.profile.cedula == r.usuario:
            if p.recurso.recurso_id == r.recurso_reservado and p.fecha_reserva == r.fecha_reserva:
                if p.hora_inicio == r.hora_inicio and p.hora_fin == r.hora_fin:
                    send_mail("Cancelacion de Reserva Especifica",
                              "Aviso de Cancelacion de Reserva, intente con las Reservas Generales",
                              settings.EMAIL_HOST_USER, [p.profile.user.email], fail_silently=False)
                    r.delete()
                    p.delete()


def ver_reservas_especifcas():
    lista_especifica = ListaReservaEspecifica.objects.all()
    pasado_manana = date.today() + timedelta(days=2)
    for r in lista_especifica:
        if r.fecha_reserva == pasado_manana:
            if verificar_hora_reserva_especifica(r.usuario, r.fecha_reserva, r.hora_inicio, r.hora_fin, r.recurso_reservado, r.prioridad) == 1:
                enviar_mensaje(r)
            if verificar_horainicio_intermedia_especifica(r.usuario, r.fecha_reserva, r.hora_inicio, r.hora_fin, r.recurso_reservado, r.prioridad) == 1:
                enviar_mensaje(r)
            if verificar_horafin_intermedia_especifica(r.usuario, r.fecha_reserva, r.hora_inicio, r.hora_fin, r.recurso_reservado, r.prioridad) == 1:
                enviar_mensaje(r)



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

            crear_form.save()  # se guardan los datos del formulario
        return redirect('rol:rol_listar')
    else:
        crear_form = RolGrupo()
    # se coloca el nombre del template y el archivo de html donde esta el formulario y el contexto del formulario
    return render(request, 'rol/crear_rol.html', {'crear_form': crear_form})


# vista basada en funciones
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




def mod_rol(request):
    return render(request, 'rol/../login/home.html')


""" Esto es de Guido n.n """


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
