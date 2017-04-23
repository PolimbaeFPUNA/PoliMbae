# -*- coding: utf-8 -*-
'''Se definen las funciones para manejar el módulo de Usuario. Se permite: crear usuario, crear una cuenta nueva,
modificar datos de Usuario y eliminar un Usuario '''
from __future__ import print_function
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import UsuarioUser
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from forms import RegistroUserForm
from django.core.mail import send_mail
from django.views.generic import ListView
from app.rol.models import Rolusuario
@login_required
def crear_user(request):
    """Permite la creacion de un usuario dentro del sistema, ingresando los datos personales del usuario
     y una contraseña. Una vez que haya sido creada, se envia la confirmación al email del solicitante"""
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
                send_mail(
                    'Acceso a Polimbae',
                    'Hola! Tu username y password es: ' + username + ',  ' + password + '. Accedé a tu cuenta para cambiar tu contraseña',
                    'polimbae@gmail.com',
                    [email],
                    fail_silently=False,
                )

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

        return render(request, "usuarios/crear_usuario.html", context)
    else:
            form= RegistroUserForm()
            context = {
                'mensaje': mensaje,
                'form': form,
            }
            return render(request, "usuarios/crear_usuario.html", context)


def valid_email( email ):
    """ Función que valida el email ingresado"""
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

@login_required
def eliminar_user(request, iduser):
    """ Permite la eliminación de un usuario. Muestra sus datos para confirmar"""
    usuario = UsuarioUser.objects.get(pk=iduser)
    mensaje = None

    if request.method == 'POST':
        id = usuario.user_id
        user = User.objects.get(pk=id)
        usuario.user.is_active = False
        usuario.user.save()
        mensaje= "El usuario fue eliminado correctamente"
    return render(request, "usuarios/eliminar_usuario.html", {'usuario': usuario, 'mensaje': mensaje})


def modificar_user(request):
    """ La vista permite que un usuario pueda modificar sus propios datos personales"""
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
    return render(request, 'usuarios/modificar_usuario.html', context)

def modificar_user_admin(request, iduser):
    """ Permite al administrador del Sistema modificar un usuario"""
    usuario = UsuarioUser.objects.get(pk=iduser)
    mensaje = None

    if request.method == 'POST':
        new_user = request.POST.get('username',False)
        new_direccion = request.POST.get('direccion',False)
        new_email= request.POST.get('email',False)
        new_telefono=request.POST.get('telefono',False)
        new_categoria= request.POST.get('categoria', False)

        if usuario.user.email != new_email:
            if User.objects.filter(email=new_email):
                mensaje = "ERROR: mail Existente"
            if not valid_email(new_email):
                if mensaje:
                    mensaje +='- El mail ingresado no es válido'
                else:
                    mensaje = 'El mail ingresado no es válido'
        if  not mensaje:
            user =UsuarioUser.objects.get(user__username=usuario.username)
            usuario.user.username=new_user
            usuario.direccion=new_direccion
            usuario.telefono=new_telefono
            usuario.user.email=new_email
            usuario.categoria= new_categoria
            usuario.user.save()
            usuario.save()
            mensaje = 'Usuario Modificado Exitosamente.'
    context = {
        'mensaje': mensaje,
        'usuario':usuario,
    }

    return render(request, 'usuarios/modificar_user_admin.html', context)

@login_required
def mod_user (request):
    """ Vista que despliega el menú del módulo de Usuario"""
    return render(request, 'usuarios/mod_usuario.html')

@login_required
def listar_user(request):
    """ Vista que despliega todos los usuarios dentro del sistema. La misma
    proporciona opciones de modificar y eliminar"""
    usuario= UsuarioUser.objects.all()

    return render(request, 'usuarios/listar_usuario.html', {'usuario': usuario})

def crear_cuenta (request):
    """ La funcion permite la creación de una cuenta sin autenticacion previa, los datos que haya ingresado se envian
    al correo del aadministrador para que el mismo se encargue de crear la cuenta """
    mensaje = None
    flag = 0
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username):
            mensaje = "Ya existe un usuario con este username"
            flag = 1
        email = request.POST['email']
        if not valid_email(email):
            flag = 1
            if not mensaje:
                mensaje = "El mail ingresado no válido"
            else:
                mensaje += " - El mail ingresado no es válido"
        if User.objects.filter(email=email):
            flag = 1
            if not mensaje:
                mensaje = "El mail ingresado ya existe"
            else:
                mensaje += " - El mail ingresado ya existe"
        if not flag:
            first_name=request.POST['nombre']
            apellido=request.POST['apellido']
            cedula=request.POST['cedula']
            direccion=request.POST['direccion']
            telefono=request.POST['telefono']
            categoria=request.POST['categoria']
            mensaje = "Espere el correo de confirmación"

            send_mail(
                'Nueva solicitud',
                'Datos del nuevo usuario: ' + username + ', ' + cedula +','+ email + ',' + first_name +','+ apellido +','+telefono+','+','+ direccion+','+ categoria +'.',
                'polimbae@gmail.com',
                ['polimbae@gmail.com'],
                fail_silently=False,
            )

    context = {
                'mensaje': mensaje,
                }
    return render(request, "login/cuenta.html", context)

@login_required
def cambiar_password(request):
    """ Función que proporciona el cambio de contraseña de un Usuario"""
    message_error1 = None
    message_error2 = None
    usuario = request.user
    if request.method == "POST":
            pass_actual = request.POST['passactual']
            if not request.user.check_password(pass_actual):
                message_error1 = 'Contraseña actual incorrecta.'
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password2 != password1:
                message_error2 = 'Las contraseñas no coinciden'
            if (message_error1 == None and message_error2 == None):
                request.user.set_password(password2)
                request.user.save()
                return render(request, 'usuarios/mod_usuario.html')

            else:
                return render(request, 'usuarios/cambiar_password.html',
                              {'message_error1': message_error1, 'message_error2': message_error2, 'usuario': usuario})
    return render(request, 'usuarios/cambiar_password.html', {'message_error1': message_error1, 'message_error2': message_error2, 'usuario': usuario})




