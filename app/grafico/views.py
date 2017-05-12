from django.shortcuts import render
import json,random
from app.mantenimiento.models import Mantenimiento
from app.recurso.models import *
from app.reserva.models import *
from django.contrib.auth.models import Group,User
from django.db.models import Count
from app.grafico.forms import MantForm
from  django.http.response import HttpResponse

# Create your views here.


def mantenimientos(request):

        mant=Mantenimiento.objects.values('tipo_recurso').annotate(c=Count('tipo_recurso')).order_by('tipo_recurso')

        tipo=TipoRecurso1.objects.all().order_by('tipo_id')
        names=[obj.nombre_recurso for obj in tipo]
        cont=[]
        for recurso in mant:
            cont.append(recurso['c'])

        context = {
            'names': json.dumps(names),
            'cont': json.dumps(cont),

        }
        return render(request, 'grafico/mantenimiento.html', context)

def reservas(request):
    res=ReservaGeneral.objects.filter(hora_inicio__range=('13:25','23:00')).values('recurso__tipo_id').annotate(c=Count('recurso__tipo_id')).order_by('recurso__tipo_id')
    cont=[]
    for reseva in res:
        cont.append(reseva['c'])

    tipo=TipoRecurso1.objects.all().order_by('tipo_id')
    names=[obj.nombre_recurso for obj in tipo]

    context={
        'names':json.dumps(names),
        'cont':json.dumps(cont),
    }

    return render(request,'grafico/reservas.html',context)