from django.shortcuts import render, redirect
from app.recurso_pr.models import *
from app.recurso_pr.forms import *
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DateDetailView, View, DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
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
            return redirect('recurso_pr:recurso_pr_listar_tipo')
    else:
        form= TipoRecursoForm()
        rform= ListCaracteristicaForm()

    return render(request, "recurso_pr/crear_tipo_recurso_pr.html", {'rform':rform, 'form':form, 'list': list_c})

def crear_recurso(request):
    lista= None
    recurso=None
    mensaje = None
    if request.method=='POST':
        try:
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
                return redirect('recurso_pr:recurso_pr_listar')
        except Exception as e:
            print (e.message, type(e))
            mensaje = "Error: No se puede guardar el registro sin elegir un tipo de Recurso"

    else:
        form= RecursoForm()

    context = {
        'lista': lista,
        'form': form,
        'mensaje':mensaje,
    }

    return render(request, "recurso_pr/crear_recurso_pr.html", context)


class ListadoTipoRecurso(ListView):
    model = TipoRecurso1
    template_name = 'recurso_pr/listar_tipo_recurso_pr.html'
    paginate_by = 10


class TipoRecursoModificar(UpdateView):
    model = TipoRecurso1
    form_class = TipoRecursoForm2
    template_name = 'recurso_pr/modificar_tipo_recurso_pr.html'
    success_url = reverse_lazy('recurso_pr:recurso_pr_listar_tipo')


class ListadoRecurso(ListView):
    model = Recurso1
    template_name = 'recurso_pr/listar_recurso.html'
    paginate_by = 10



class RecursoModificar(UpdateView):
    model = Recurso1
    form_class = RecursoForm
    template_name = 'recurso_pr/modificar_recurso.html'
    success_url = reverse_lazy('recurso_pr:recurso_pr_listar')


class ModificarCaracteristicas(UpdateView):
    model = Caracteristica
    form_class = CaracteristicaForm
    template_name = 'recurso_pr/modificar_caracteristicas.html'
    success_url = reverse_lazy('recurso_pr:recurso_pr_listar')


def lista_caracteristica(request, recurso_id):
    caracteristica = DescripCarac.objects.filter(recurso__recurso_id=recurso_id)
    contexto = {'caracteristica': caracteristica}
    return render(request, 'recurso_pr/lista_caracteristica.html', contexto)


def modificar_caracteristicas(request, ctra_id):
    caracteristica = Caracteristica.objects.get(ctra_id=ctra_id)
    if request.method == 'GET':
        form = CaracteristicaForm(instance=caracteristica)
    else:
        form = CaracteristicaForm(request.POST, instance=caracteristica)
        if form.is_valid():
            form.save()
        return redirect('recurso_pr:recurso_pr_listar')
    return render(request, 'recurso_pr/modificar_caracteristicas.html', {'form': form})
