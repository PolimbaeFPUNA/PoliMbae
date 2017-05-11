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
