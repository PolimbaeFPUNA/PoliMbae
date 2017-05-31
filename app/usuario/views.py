# -*- coding: utf-8 -*-
'''Se definen las funciones para manejar el módulo de Usuario. Se permite: crear usuario, crear una cuenta nueva,
modificar datos de Usuario y eliminar un Usuario '''
from __future__ import print_function
from __future__ import unicode_literals
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from app.usuario.models import Profile, CategoriaUsuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from app.usuario.forms import *
from app.usuario.models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
import hashlib, datetime, random
from app.rol.models import PermisoRol, UserRol
from django.contrib.auth.models import Group
from django.core.mail import send_mail

''' Crear cuenta desde fuera del sistema '''
def register_user(request):
    """Se cuentan con dos formularios:
    form = para crear el objeto del tipo User, modelo por defecto de Django para manejo de Users
    form_usuario = para capturar datos de la persona, como telefono, direccion, cedula de identidad.
    El modelo UserProfile es utilizado para el manejo de activacion de cuenta del usuario. Si
    el mismo no es activado por el administrador, el usuario no puede aceder al sistema, ya que
    se encuentra inactivo.
    El periodo de activacion de la cuenta es de 2 dias, luego de esto, no podra activarse en ninguna forma."""
    mensaje = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        usuario = request.POST['cedula']
        if form.is_valid() and form_usuario.is_valid():
            form.save()  # guardar el usuario en la base de datos si es válido
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Obtiene el nombre de usuario
            user = User.objects.get(username=username)
            # Crea el perfil del usuario
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()
            if verificar_cedula(usuario) == 1:
                mensaje = "Error: Ya existe un usuario registrado con el mismo CI"
            if not mensaje:
                Profile.objects.create(user=user, direccion=request.POST['direccion'], telefono=request.POST['telefono'], cedula=request.POST['cedula'])
            return render(request, 'login/register_success.html')
    else:
        form = RegistrationForm()
        form_usuario = UsuarioForm()
    return render(request, 'login/cuenta_crear.html', {'form': form, 'form2': form_usuario})


'''Activar Cuenta desde la lista de Cuentas Pendientes del Sistema.
Se recibe el request y el user_id sobre el cual se efectuara la activacion.

    user1 es el usuario dentro del modelo que maneja la activacion de la cuenta: UserProfile
    user2: utilizado para identificar al mismo usuario dentro del modelo User que trae Django por defecto.
    Se llama a la funcion register_confirm() para activar la cuenta con el key de activacion:activation_key
    Luego, se envia un correo al usuario confirmando su activacion y la posibilidad de Loguaerse para acceso al sistema
 '''
def activar_cuenta(request, user):
    user1 = get_object_or_404(UserProfile, id=user)
    user2 = get_object_or_404(User, id=user1.user_id)
    mensaje = None
    if register_confirm(user1.activation_key) == 1:
        mensaje  = "Error: El tiempo de espera para la activacion a expirado"
    if not mensaje:
        # Envia un email de confirmación
        email_subject = 'Confirmacion de Cuenta'
        email_body = "Hola %s, Gracias por registrarte. Tu cuenta ha sido activada, ahora ya puedes loguearte, confirma tu correo haciendo clic aqui: http://127.0.0.1:8000/usuarios/confirm/%s" % (
        user2.username, user1.activation_key)
        send_mail(email_subject, email_body, 'polimbae@gmail.com', [user2.email], fail_silently=False)
        user1.delete()
        return redirect('usuarios:listaruser')


'''En caso de no aprobarse la cuenta solicidata se elimina del sistema los registros de Cuentas
UserProfile para la activacion
User manejado por Django para logueo al sistema
Profile que contiene datos comunes del usuario (telefono, direccion, ect)'''

def desactivar_user(request, user):
    user1 = get_object_or_404(UserProfile, id=user)
    user2 = get_object_or_404(User, id=user1.user_id)
    profile = get_object_or_404(Profile, id=user2.id)
    profile.delete()
    user1.delete()
    user2.delete()
    return redirect('usuarios:listaprofile')

'''Una vez confirmado desde el correo por el usuario'''
def confirmar(request, activation_key):
    return HttpResponseRedirect('/login/')


'''Funcion para confirmar el ingreso del nuevo usuario al sistema.
Esta funcion es utilizada en la funcion activar_cuenta(request, user).'''

def register_confirm(activation_key):
    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        return 1
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    return 0


'''Lista de Cuentas creadas desde el fuera del sistema, esperando ser
activadas por el administrador, antes de 48 horas'''

class ListaUserProfile(ListView):
    model = UserProfile
    template_name = 'usuarios/lista_activados.html'


'''Listas de Usuarios ya registrados en el sistema '''

class ListarUser (ListView):
    model = Profile
    template_name = 'usuarios/listar_usuario.html'


'''Verifica si ya exite un usuario registrado con el mismo numero de cedula'''


def verificar_cedula(usuario):
    """user: Lista todos los objetos del modelo Profile
        u: para comparar la cedula del usuario registrado con la cedula nueva
        returna 1 si existe un CI, por lo tanto es conciderado un error
        retorna 0 si no existe registrado un usuario con el mismo CI"""
    user = Profile.objects.all()
    for u in user:
        if u.cedula == usuario:
            return 1
    return 0


class ModificarUser (UpdateView):
    model= Profile
    second_model = User
    template_name = 'usuarios/modificar_usuario.html'
    form_class = UsuarioForm
    second_form_class = UserEditable
    success_url = reverse_lazy('usuarios:listaruser')
    def get_context_data(self, **kwargs):
        context = super(ModificarUser, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        usuario= self.model.objects.get(id=pk)
        user= self.second_model.objects.get(id=usuario.user_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance= user)
            context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_usuario = kwargs['pk']
        usuario = self.model.objects.get(id=id_usuario)
        user = self.second_model.objects.get(id=usuario.user_id)
        form = self.form_class(request.POST, instance=usuario)
        form2 = self.second_form_class(request.POST, instance=user)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class EliminarUser(DeleteView):
    model = Profile
    template_name = 'usuarios/eliminar_usuario.html'
    success_url = reverse_lazy('usuarios:listaruser')


class CrearCategoria(CreateView):
    model = CategoriaUsuario
    form_class = CategoriaForm
    template_name = 'usuarios/categoria_crear.html'
    success_url = reverse_lazy('usuarios:crear_categoria')


class ListarCategoria (ListView):
    model = CategoriaUsuario
    template_name = 'usuarios/listar_categoria.html'


def asignar_categoria(request, user):
    usuario = Profile.objects.get(user_id=user)
    if request.method == 'GET':
        form = UsuariocategoriaForm(instance=usuario)
    else:
        form = UsuariocategoriaForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
        return redirect('usuarios:listaruser')
    return render(request, 'usuarios/asignar_categoria.html', {'form': form})

class Asignar (UpdateView):
    model = User
    template_name = 'usuarios/asignar.html'
    success_url = reverse_lazy('usuarios:listaruser')

    def get_initial(self):
        initial = super(Asignar, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_form_class(self):
        return AsignarForm

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(Asignar, self).form_valid(form)

