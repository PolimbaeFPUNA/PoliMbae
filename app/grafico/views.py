from django.shortcuts import render
import json,random
from app.mantenimiento.models import Mantenimiento
from app.recurso.models import *
from app.reserva.models import *
from django.contrib.auth.models import Group,User
from django.db.models import Count
from app.grafico.forms import ReservaForm,ReservaForm2,MantForm
from  django.http.response import HttpResponse

# Create your views here.


def mantenimientos(request):
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
        mant = Mantenimiento.objects.filter(fecha_entrega__range=('2017-05-01', '2017-08-30')).filter(fecha_fin__range=('2017-05-01', '2017-08-30')).values(
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
    if request.method=='POST':
        form=ReservaForm(request.POST)
        fecha1 =request.POST['fecha_reserva']
        hora1=request.POST['hora_inicio']
        hora2=request.POST['hora_fin']
        res = ReservaGeneral.objects.filter(
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
        res=ReservaGeneral.objects.filter(hora_inicio__range=('13:25','23:00')).values('recurso__tipo_id').annotate(c=Count('recurso__tipo_id')).order_by('recurso__tipo_id')
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
    res=Recurso1.objects.filter(estado='DI').values('estado').annotate(c=Count('tipo_id')).order_by('tipo_id')
    cont=[]
    for reseva in res:
        cont.append(reseva['c'])

    tipo=TipoRecurso1.objects.all().order_by('tipo_id')
    names=[obj.nombre_recurso for obj in tipo]

    context={
        'names':json.dumps(names),
        'cont':json.dumps(cont),
    }

    return render(request,'grafico/recursos.html',context)