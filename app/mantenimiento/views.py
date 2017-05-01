from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from app.mantenimiento.models import Mantenimiento
from app.mantenimiento.forms import *
from django.core.urlresolvers import reverse_lazy
from app.recurso.models import TipoRecurso1, Recurso1
from django.forms import formset_factory
from django.utils.dateparse import parse_time, parse_datetime, parse_date
from app.reserva.models import *


def listar_mantenimiento(request):
    mant= Mantenimiento.objects.all().order_by('id')

    return render(request, "mantenimiento/listar_mantenimiento.html", {"mant":mant})


def crear_mantenimiento(request):
    rform= None
    mensaje= None
    if request.method == 'POST':
        form= MantForm(request.POST)

        if request.POST.get('listar'):

            rform=ListRecursoForm(tipo=request.POST['tipo_recurso'])

        if request.POST.get('guardar'):
            fecha_entrega= request.POST['fecha_entrega']
            fecha_fin= request.POST['fecha_fin']
            if verificar_hora_fecha(fecha_entrega, fecha_fin):
                mensaje = "Verifique fechas y horas"
            if not mensaje:
                recurso= Recurso1.objects.get(recurso_id=request.POST['lista'])
                rtipo= TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])

                Mantenimiento.objects.create(tipo_recurso=rtipo,recurso=recurso,
                                         fecha_entrega=request.POST['fecha_entrega'], fecha_fin=request.POST['fecha_fin'],
                                         tipo= request.POST['tipo'], resultado= request.POST['resultado'])
                #verificar_reservas(fecha_entrega,fecha_fin,recurso)
            return redirect("mantenimiento:mantenimiento_listar")

    else:
        form= MantForm()
        rform=ListRecursoForm(tipo=-1)

    context ={'form':form, 'rform':rform, 'mensaje':mensaje}
    return render(request, 'mantenimiento/crear_mantenimiento.html', context)


def modificar_mantenimiento(request, pk):
    mensaje= None
    mant= Mantenimiento.objects.get(pk=pk)
    list_tipo= TipoRecurso1.objects.all()
    list_recurso= Recurso1.objects.filter(tipo_id=mant.tipo_recurso)
    form = ChoiceForm(instance=mant)
    if request.method == 'POST':
        tipo_recurso= TipoRecurso1.objects.get(nombre_recurso=request.POST.get('tipo_recurso'))
        recurso= Recurso1.objects.get(recurso_id=request.POST.get('recurso'))
        fecha_entrega= request.POST.get('fecha_entrega')
        fecha_fin= request.POST.get('fecha_fin')
        tipo= request.POST.get('tipo')
        resultado= request.POST.get('resultado')
        if verificar_hora_fecha(fecha_entrega,fecha_fin):
            mensaje= "Verifique fechas y horas"

        if not mensaje:
            mant.tipo_recurso = tipo_recurso
            mant.recurso = recurso
            mant.fecha_entrega = fecha_entrega
            mant.fecha_fin = fecha_fin
            mant.tipo= tipo
            mant.resultado= resultado
            mant.save()
            return redirect("mantenimiento:mantenimiento_listar")
    context = {'mant': mant, 'list': list_tipo, 'rlist': list_recurso, 'form':form, 'mensaje': mensaje}
    return render(request, 'mantenimiento/modificar_mantenimiento.html',context )

class EliminarMant(DeleteView):
    model= Mantenimiento
    template_name= "mantenimiento/eliminar_mantenimiento.html"
    success_url = reverse_lazy("mantenimiento:mantenimiento_listar")

''' Funcion que sirve para verificar si se ha ingresado una hora de inicio mayor a la hora de finalizacion y
las fechas iguales, o si la fecha de entrega es mayor que la fecha de finalizacion
'''
def verificar_hora_fecha(date_time_inicio, date_time_fin):
    aux_1 = parse_datetime(date_time_inicio)
    f1= aux_1.strftime('%Y-%m-%d')
    h1= aux_1.strftime('%H:%M:%S')
    aux_2 = parse_datetime(date_time_fin)
    f2= aux_2.strftime('%Y-%m-%d')
    h2= aux_2.strftime('%H:%M:%S')
    if f2==f1 and h2 <= h1:
        return True
    elif f2<f1:
        return True
    else:
        return False






