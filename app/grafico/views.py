from django.shortcuts import render
import json,random
from app.mantenimiento.models import Mantenimiento
from app.recurso_pr.models import *
from app.reserva_new.models import *
from django.contrib.auth.models import Group,User
from django.db.models import Count
from app.grafico.forms import ReservaForm,ReservaForm2,MantForm
from  django.http.response import HttpResponse

# Create your views here.


def mantenimientos(request):
    """funcion que recibe dos fechas, obtiene todos los recursos con mantenimiento
    en ese rango de fechas para generar un grafico"""
    if request.method=='POST':
        form=MantForm(request.POST)
        fecha_ini=request.POST['fecha_entrega']
        fecha_fin = request.POST['fecha_fin']

        mant=Mantenimiento.objects.filter(fecha_entrega__range=(fecha_ini,fecha_fin)).values('tipo_recurso').annotate(c=Count('tipo_recurso')).order_by('tipo_recurso')

        tipo=TipoRecurso1.objects.all().order_by('tipo_id')
        names=[obj.nombre_recurso for obj in tipo]
        cont=[]
        for recurso in mant:
            cont.append(recurso['c'])

        context = {
            'names': json.dumps(names),
            'cont': json.dumps(cont),
            'form':form,
        }
        return render(request, 'grafico/mantenimiento.html', context)
    else:
        form=MantForm()
        mant = Mantenimiento.objects.filter(fecha_entrega__range=('2017-01-01', '2017-12-30')).filter(fecha_fin__range=('2017-05-01', '2017-08-30')).values(
            'tipo_recurso').annotate(c=Count('tipo_recurso')).order_by('tipo_recurso')

        tipo = TipoRecurso1.objects.all().order_by('tipo_id')
        names = [obj.nombre_recurso for obj in tipo]
        cont = []
        for recurso in mant:
            cont.append(recurso['c'])
        context = {
            'names': json.dumps(names),
            'cont': json.dumps(cont),
            'form': form,
        }

    return render(request, 'grafico/mantenimiento.html',context)

def reservas(request):
    """funcion que recibe dos fechas, obtiene todos los recursos con reservas
        en esa fecha y en el rango de horas para generar un grafico"""
    if request.method=='POST':
        form=ReservaForm(request.POST)
        fecha1 =request.POST['fecha_reserva']
        hora1=request.POST['hora_inicio']
        hora2=request.POST['hora_fin']
        res = Reserva.objects.filter(
            fecha_reserva=fecha1).filter(hora_inicio__range=(hora1,hora2)).filter(
            hora_fin__range=(hora1,hora2)).values('recurso__tipo_id').annotate(
            c=Count('recurso__tipo_id')).order_by('recurso__tipo_id')
        cont = []
        for reseva in res:
            cont.append(reseva['c'])

        tipo = TipoRecurso1.objects.all().order_by('tipo_id')
        names = [obj.nombre_recurso for obj in tipo]

        context = {
            'names': json.dumps(names),
            'cont': json.dumps(cont),
            'form':form,
        }

        return render(request, 'grafico/reservas.html', context)
    else:
        form=ReservaForm()
        res=Reserva.objects.filter(hora_inicio__range=('06:00','23:59')).values('recurso__tipo_id').annotate(c=Count('recurso__tipo_id')).order_by('recurso__tipo_id')
        cont=[]
        for reseva in res:
            cont.append(reseva['c'])

        tipo=TipoRecurso1.objects.all().order_by('tipo_id')
        names=[obj.nombre_recurso for obj in tipo]

        context={
            'names':json.dumps(names),
            'cont':json.dumps(cont),
            'form': form,
        }

        return render(request,'grafico/reservas.html',context)

def recursos(request):
    """funcion que recibe dos fechas, obtiene todos los recursos disponibles
        en el dia para generar un grafico"""
    res=Recurso1.objects.filter(estado='DI').values('estado').annotate(c=Count('tipo_id')).order_by('tipo_id')
    cont=[]
    color=[]

    for reseva in res:
        r = lambda: random.randint(0, 255)
        color.append('#%02X%02X%02X' % (r(),r(),r()))
        cont.append(reseva['c'])


    tipo=TipoRecurso1.objects.all().order_by('tipo_id')
    names=[obj.nombre_recurso for obj in tipo]


    context={
        'names':json.dumps(names),
        'cont':json.dumps(cont),
        'color':json.dumps(color)
    }

    return render(request,'grafico/recursos.html',context)