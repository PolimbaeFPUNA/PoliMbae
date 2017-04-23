# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from app.recurso.models import Recurso
from app.recurso.models import TipoRecurso
import random


def crear_rec(request):
    """Se crea un recurso a partir de un tipo de recurso existente"""
    mensaje = None
    flag = 0
    if request.method == "POST":
        nombre_rec= request.POST['nombre_rec']
        if TipoRecurso.objects.filter(nombre_rec = 'nombre_rec'):
            flag = 1
            tiporecurso = TipoRecurso.objects.filter(nombre_rec='nombre_rec')
            Recurso.objects.create(tipo_rec= tiporecurso, estado=request.POST['estado'])
            mensaje = "Recurso Creado"

        if not flag:
            mensaje = "Tipo de recurso inexistente"

    context = {
        'mensaje': mensaje,
    }
    return render(request, "recurso/crear_recurso.html", context)


def eliminar_rec(request, codigo_rec):
    """Se elimina un recurso especifico"""
    recurso = Recurso.objects.get(pk=codigo_rec)
    mensaje = None
    if request.method == 'POST':
        rec = Recurso.objects.get(pk=codigo_rec)
        rec.is_active = False
        rec.save()
        mensaje="El recurso fue eliminado correctamente"
    return render(request, "recurso/eliminar_recurso.html", {'recurso': recurso, 'mensaje': mensaje})


def mod_rec (request):
    return render(request, 'recurso/mod_recurso.html')


def listar_rec(request):
    recurso = Recurso.objects.all()
    return render(request, 'recurso/listar_recurso.html', {'recurso': recurso})
