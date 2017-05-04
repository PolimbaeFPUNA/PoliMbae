# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from forms import LoginForm
from django.contrib.auth.decorators import login_required


def Login(request):

    message = None
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect(next)

                else:
                    message = "Usuario Inactivo"
            else:
                message = "Datos Incorrectos"
    else:
        form = LoginForm()

    return render(request, "login/login.html", {'redirect_to': next, 'message': message, 'form': form})



def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

