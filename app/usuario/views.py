# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import UsuarioUser
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from forms import RegistroUserForm

@login_required
def registrar_user(request):
    mensaje= None
    flag= 0
    if request.method == "POST":
        form= RegistroUserForm(request.POST)
        if form.is_valid():
            cedula = request.POST['cedula']
            username = request.POST['username']
            if User.objects.filter(username=username):
                mensaje = "El username ya existe"
                flag=1
            email= request.POST['email']
            if not valid_email(email):
                flag=1
                if not mensaje:
                    mensaje= "El mail no es válido"
                else:
                    mensaje= "- El mail no es válido"
            if User.objects.filter(email=email):
                flag=1
                if not mensaje:
                    mensaje= "El mail ya existe"
                else:
                    mensaje="-El mail ya existe"
            password= request.POST['password']
            password2 = request.POST['password2']
            if password != password2:
                if not mensaje:
                    mensaje = "Las contraseñas no coinciden"
                else:
                    mensaje += " - Las contraseñas no coinciden"
                flag = 1
            if not flag:
                user = User.objects.create_user(username=username, first_name=request.POST['nombre'],
                                                email=request.POST['email'],
                                                last_name=request.POST['apellido'], password=request.POST['password'])
                UsuarioUser.objects.create(user=user, cedula=cedula, direccion=request.POST['direccion'],
                                           telefono=request.POST['telefono'],
                                           categoria=request.POST['categoria'])
                mensaje = "Guardado exitoso"
        context = {
            'mensaje': mensaje,
            'form': form,
        }

        return render(request, "crear_usuario.html", context)
    else:
            form= RegistroUserForm()
            context = {
                'mensaje': mensaje,
                'form': form,
            }
            return render(request, "crear_usuario.html", context)


def valid_email( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def eliminar_user(request, iduser):
    usuario = UsuarioUser.objects.get(pk=iduser)
    mensaje = None
    print(usuario.user.is_active)
    if request.method == 'POST':
        id = usuario.user_id
        user = User.objects.get(pk=id)
        usuario.user.is_active = False
        usuario.user.save()
        mensaje= "El usuario fue eliminado correctamente"


    return render(request, "eliminar_usuario.html", {'usuario': usuario, 'mensaje': mensaje})

def modificar_user(request):
    mensaje = None
    usuario = request.user
    user = UsuarioUser.objects.get(user__username=usuario.username)

    if request.method == 'POST':
        new_user = request.POST.get('username',False)
        new_direccion = request.POST.get('direccion',False)
        new_email= request.POST.get('email',False)
        new_telefono=request.POST.get('telefono',False)
        new_categoria= request.POST.get('categoria', False)

        if usuario.email != new_email:
            if User.objects.filter(email=new_email):
                mensaje = "ERROR: mail Existente"
            if not valid_email(new_email):
                if mensaje:
                    mensaje +='- El mail ingresado no es válido'
                else:
                    mensaje = 'El mail ingresado no es válido'
        if  not mensaje:
            user =UsuarioUser.objects.get(user__username=usuario.username)
            user.user.username=new_user
            user.direccion=new_direccion
            user.telefono=new_telefono
            user.user.email=new_email
            user.categoria= new_categoria
            user.user.save()
            user.save()
            mensaje = 'Usuario Modificado Exitosamente.'
    context = {
        'mensaje': mensaje,
        'usuario':user,
    }

    return render(request,'modificar_usuario.html', context)
@login_required
def mod_user (request):
    return render(request, 'mod_usuario.html')

def listar_user(request):
    usuario= UsuarioUser.objects.all()

    return render(request, 'listar_usuario.html', {'usuario': usuario})
