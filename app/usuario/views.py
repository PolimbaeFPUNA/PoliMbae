# -*- coding: utf-8 -*-
'''Se definen las funciones para manejar el módulo de Usuario. Se permite: crear usuario, crear una cuenta nueva,
modificar datos de Usuario y eliminar un Usuario '''
from __future__ import print_function
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from app.usuario.models import Profile, CategoriaUsuario
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from app.usuario.forms import UsuarioForm, UserForm, CategoriaForm, UserEditable, AsignarForm

from django.core.mail import send_mail
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from app.rol.models import PermisoRol, UserRol
from django.contrib.auth.models import Group





def crear_user(request):
    mensaje= None

    if request.method == "POST":
        form_usuario= UsuarioForm(request.POST)
        form_user= UserForm(request.POST)
        usuario = request.POST['cedula']
        if form_usuario.is_valid() and form_user.is_valid():

            pass1= request.POST['password']
            pass2=request.POST['password2']
            if pass1 != pass2:
                mensaje="-Las Contraseñas no coinciden"
            if verificar_cedula(usuario) == 1:
                mensaje = "Error: Ya existe un usuario registrado con el mismo CI"
            if not mensaje:
                user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['first_name'],
                                            email=request.POST['email'],
                                            last_name=request.POST['last_name'], password=request.POST['password'])
                categoria= CategoriaUsuario.objects.filter(id=request.POST['categoria']).get()
                Profile.objects.create(user=user, direccion=request.POST['direccion'],telefono=request.POST['telefono'], categoria=categoria, cedula=request.POST['cedula'])
                return redirect('usuarios:listaruser')
    else:
        form_user = UserForm()
        form_usuario= UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form_user': form_user, 'form_usuario': form_usuario, 'mensaje': mensaje})

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

class EliminarCategoria(DeleteView):
    model = CategoriaUsuario
    template_name = 'usuarios/eliminar_categoria.html'
    success_url = reverse_lazy('usuarios:listar_categoria')

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

