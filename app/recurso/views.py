
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from app.recurso.models import Recurso1, TipoRecurso1, Caracteristica
from app.recurso.forms import RecursoForm, TipoRecursoForm, CaractiristicaForm, RecursoForm2, TipoRecursoForm2
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import string

""" Para Funciones y clases para Listar Recurso """


def recurso_listar(request):
    """ Funcion que Lista todos los registros creados del modelo Rolusuario y los envia al template listar_rol.html"""
    qrecurso = RecursoForm.objects.all().order_by('id')
    contexto = {'recurso': qrecurso}
    return render(request, 'recurso/listar_recurso.html', contexto)


class RecursoListar(ListView):
    model = Recurso1
    template_name = 'recurso/listar_recurso.html'
    paginate_by = 10


""" Para Funciones y clases para Listar Tipo de Recurso """


def tipo_recurso_listar(request):
    qtipo = TipoRecursoForm2.objects.all().order_by('id')
    contexto = {'tiporecurso': qtipo}
    return render(request, 'recurso/listar_tiporecurso.html', contexto)


class TipoRecursoListar(ListView):
    model = TipoRecurso1
    template_name = 'recurso/listar_tiporecurso.html'
    paginate_by = 10


def caracteristica_listar(request):
    qcrta = Caracteristica.objects.all().order_by('id')
    contexto = {'caracteristica': qcrta}
    return render(request, 'recurso/caracteristica_listar.html', contexto)


class CaracteristicaListar(ListView):
    model = Caracteristica
    template_name = 'recurso/caracteristica_listar.html'
    paginate_by = 10

""" Para Clases para Crear Recurso y Tipo de Recurso """


class TipoRecursoCrtaCrear(CreateView):
    model = TipoRecurso1
    template_name = 'recurso/crear_tipo_recurso.html'
    form_class = TipoRecursoForm
    second_form_class = CaractiristicaForm
    success_url = reverse_lazy('recurso:tiporecurso_listar')

    def get_context_data(self, **kwargs):
        context = super(TipoRecursoCrtaCrear, self).get_context_data(**kwargs)
        if 'form_tiporecurso' not in context:
            context['form_tiporecurso'] = self.form_class(self.request.GET)
        if 'form_crta' not in context:
            context['form_crta'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form_tiporecurso = self.form_class(request.POST)
        form_crta = self.second_form_class(request.POST)
        if form_tiporecurso.is_valid() and form_crta.is_valid():
            tiporecurso = form_tiporecurso.save(commit=False)
            tiporecurso.ctra_id = form_crta.save()
            tiporecurso.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form_tiporecurso, form2=form_crta))


class RecursoEstadoCrear(CreateView):
    model = Recurso1
    form_class = RecursoForm
    template_name = 'recurso/crear_recurso.html'
    success_url = reverse_lazy('recurso:recurso_listar')


""" Para Clases para Modificar Tipo de Recurso """


class TipoRecursoModificar(UpdateView):
    model = TipoRecurso1
    form_class = TipoRecursoForm
    template_name = 'recurso/modificar_tipo.html'
    success_url = reverse_lazy('recurso:tiporecurso_listar')


class CaracteristicaModificar(UpdateView):
    model = Caracteristica
    form_class = CaractiristicaForm
    template_name = 'recurso/modificar_caracteristica.html'
    success_url = reverse_lazy('recurso:tiporecurso_listar')


class RecursoModificar(UpdateView):
    model = Recurso1
    form_class = RecursoForm
    template_name = 'recurso/crear_recurso.html'
    success_url = reverse_lazy('recurso:recurso_listar')

'''Busca los recursos segun el nombre del tipo de recurso'''


def buscar_recurso(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            recursos = Recurso1.objects.filter(tipo_id__nombre_recurso__icontains=q)
            return render(request, 'recurso/consultar_recurso.html', {'recursos': recursos, 'query': q})
    return render(request, 'recurso/consultar_recurso.html', {'error': error})


