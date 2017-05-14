from django.shortcuts import render, redirect
from app.recurso_pr.models import *
from app.recurso_pr.forms import *
# Create your views here.



def crear_tipo_recurso(request):
    rform= None
    form= None
    list_c = None
    if request.method == 'POST':
        form= TipoRecursoForm(request.POST)

        if request.POST.get('crear'):

            Caracteristica.objects.create(nombre_caracteristica=request.POST['caracteristica'])
            rform=ListCaracteristicaForm()

        if request.POST.get('guardar'):
            nombre_recurso = request.POST['nombre_recurso']
            reservable = request.POST['reservable']
            if reservable=='on':
                r= True
            else:
                r=False
            tipo = TipoRecurso1.objects.create(nombre_recurso=nombre_recurso, reservable=r)
            list= Caracteristica.objects.filter(tipo_recurso__isnull=True)
            for l in list:
                l.tipo_recurso= tipo
                l.save()
    else:
        form= TipoRecursoForm()
        rform= ListCaracteristicaForm()

    return render(request, "recurso_pr/crear_tipo_recurso_pr.html", {'rform':rform, 'form':form, 'list': list_c})

def crear_recurso(request):
    lista= None
    recurso=None
    if request.method=='POST':
        form= RecursoForm(request.POST)
        tipo_id= request.POST['tipo_id']
        estado= request.POST['estado']
        tipo= TipoRecurso1.objects.get(tipo_id=tipo_id)
        if request.POST.get('agregar'):
           lista= Caracteristica.objects.filter(tipo_recurso=request.POST['tipo_id'])

        if request.POST.get('guardar'):
            recurso = Recurso1.objects.create(tipo_id=tipo, estado=estado)
            lista = Caracteristica.objects.filter(tipo_recurso=request.POST['tipo_id'])
            for l in lista:
                descripcion = request.POST['descripcion'+str(l.pk)]
                caracteristica= Caracteristica.objects.filter(nombre_caracteristica=request.POST['caracteristica'+str(l.pk)]).get(tipo_recurso__tipo_id=tipo_id)
                description= DescripCarac.objects.create(recurso=recurso,descripcion=descripcion, ctra_id= caracteristica)
                caracteristica.descripcion= description.descripcion
                caracteristica.save()
    else:
        form= RecursoForm()

    return render(request, "recurso_pr/crear_recurso_pr.html", {'lista':lista, 'form':form})

