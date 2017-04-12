
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from usuario.models import UserProfile
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, send_mass_mail

def registrarUser(request):
    mensaje = None
    flag = 0
    if request.method == "POST":
        # verificamos que el usuario no exista en la BD
        username = request.POST['username']
        if User.objects.filter(username=username):
            mensaje = "Ya existe un usuario con este username"
            flag = 1
        email = request.POST['email']
        if not ValidateEmail(email):
            flag = 1
            if not mensaje:
                mensaje = "El mail ingresado no es correcto"
            else:
                mensaje += " - El mail ingresado no es correcto"
        if User.objects.filter(email=email):
            flag = 1
            if not mensaje:
                mensaje = "El mail ingresado ya ha sido registrado"
            else:
                mensaje += " - El mail ingresado ya ha sido registrado"
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            if not mensaje:
                mensaje = "Las contrasenhas no coinciden"
            else:
                mensaje += " - Las contrasenhas no coinciden"
            flag = 1
        if not flag:

            user = User.objects.create_user(username=username, first_name=request.POST['nombre'],
                                            email=request.POST['email'],
                                            last_name=request.POST['apellido'], password=request.POST['password'])

            UserProfile.objects.create(user=user, direccion=request.POST['direccion'],
                                       telefono=request.POST['telefono'],
                                       categoria=request.POST['categoria'])
            mensaje = "Guardado exitoso"

    context = {
        'mensaje': mensaje,
    }
    return render(request, "CrearUsuario.html", context)

def ValidateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


