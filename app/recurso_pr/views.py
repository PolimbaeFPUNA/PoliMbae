from django.shortcuts import render, redirect
from app.log.models import *
from app.recurso_pr.forms import *
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DateDetailView, View, DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

'''Crear Tipo de Recurso y Nombres de las Caracteristicas Configurables que deberan ser definidas en los Recursos'''

def crear_tipo_recurso(request):
    """Se crea un tipo de recurso con el uso del Formulario TipoRecursoForm, que contiene:
        nombre_recurso (del tipo Text) y la indicacion de recurso reservable, con valor Booleamno
        Se definen los nombres de las Caracteristicas configurables que en el Recurso deberan ser definidos/
        Si el metodo es Post, se guardan dichos datos y se crean las Caracteristicas del Tipo de Recurso
        Si el metodo es Get, se eliminan las caracteristicas sin vinculacion con algun Tipo de Recurso
        y no se guarda ningun objeto de Tipo de Recurso."""
    rform= None
    form = None
    list_c = None
    mensaje = None
    if request.method == 'POST':
        form= TipoRecursoForm(request.POST)
        if request.POST.get('crear'):

            Caracteristica.objects.create(nombre_caracteristica=request.POST['caracteristica'])
            rform=ListCaracteristicaForm()
            mensaje = "Caracteristica Agregada! Puede seguir agregando mas Caracteristicas"

        if request.POST.get('guardar'):
            nombre_recurso = request.POST['nombre_recurso']
            reservable = request.POST.get('reservable', False)
            if reservable == 'on':
                    reservable= True
            else:
                    reservable= False
            tipo = TipoRecurso1.objects.create(nombre_recurso=nombre_recurso, reservable=reservable)

            Log.objects.create(usuario=request.user,fecha_hora=datetime.now(),mensaje='Crear Tipo de Recurso'+tipo.__str__())
            list= Caracteristica.objects.filter(tipo_recurso__isnull=True)
            for l in list:
                l.tipo_recurso = tipo
                l.save()
            return redirect('recurso_pr:recurso_pr_listar_tipo')
        if request.POST.get('cancelar'):
            caract = Caracteristica.objects.filter(tipo_recurso__isnull=True)
            for c in caract:
                 c.delete()
            return redirect('recurso_pr:recurso_pr_listar_tipo')
    else:
        form= TipoRecursoForm()
        rform= ListCaracteristicaForm()

    context = {
        'rform': rform,
        'form': form,
        'list': list_c,
        'mensaje': mensaje,
    }
    return render(request, "recurso_pr/crear_tipo_recurso_pr.html", context)

'''Crear Recurso a partir de un Tipo de Recurso seleccionado.
    Ademas se definen los valores de las caracteristicas del Recurso. '''


def crear_recurso(request):
    """Crea un recurso con una caracteristicas configurables
    Formulario utilizado RecursoForm.
    tipo_id: gurada el id del tipo de recurso
    estado: guarda el estado seleccionado
    tipo: guarda el tipo de recurso con el metodo get
    lista: guarda todas las caracteristicas filtradas del tipo de recurso
    Si el metodo es Post, se guardan dichos detos y se cargan los valores de las caracteristicas en un
    objeto del modelo Caracateristica.
    Se redirecciona a la lista de Recursos una vez creados los objetos de Recuros y Caracteristicas
    El Template utilizado es crear_recurso_pr.html"""

    lista= None
    recurso=None
    mensaje = None
    form = None
    if request.method =='POST':
        try:
            form = RecursoForm(request.POST)
            tipo_id = request.POST['tipo_id']
            tipo = TipoRecurso1.objects.get(tipo_id=tipo_id)
            if request.POST.get('agregar'):
                lista = Caracteristica.objects.filter(tipo_recurso=request.POST['tipo_id'])

            if request.POST.get('guardar'):
                recurso = Recurso1.objects.create(tipo_id=tipo, descripcion=request.POST['descripcion'])
                lista = Caracteristica.objects.filter(tipo_recurso=request.POST['tipo_id'])
                for l in lista:
                    descripcion = request.POST['descripcion'+str(l.pk)]
                    caracteristica = Caracteristica.objects.filter(nombre_caracteristica=request.POST['caracteristica'+str(l.pk)]).get(tipo_recurso__tipo_id=tipo_id)
                    description = DescripCarac.objects.create(recurso=recurso,descripcion=descripcion, ctra_id=caracteristica)
                    caracteristica.descripcion= description.descripcion
                    caracteristica.save()

                Log.objects.create(usuario=request.user, fecha_hora=datetime.now(),
                                   mensaje='Crear Recurso' + recurso.__str__())
                return redirect('recurso_pr:recurso_pr_listar')
        except Exception as e:
            print (e.message, type(e))
            mensaje = "Error: Existen campos sin completar."
    else:
        form = RecursoForm()
        caract = Caracteristica.objects.all()
        for c in caract:
            if c.tipo_recurso == " ":
                c.delete()
            if c.nombre_caracteristica == "":
                c.delete()
    context = {
        'lista': lista,
        'form': form,
        'mensaje': mensaje,
    }
    return render(request, "recurso_pr/crear_recurso_pr.html", context)


'''Lista de Tipo de Recursos Existentes con el uso del view ListView'''


class ListadoTipoRecurso(ListView):
    """Modelo utilizado de TipoRecurso1
    template listar_tipo_recurso_pr.html
    paginacion de 10 registros"""
    model = TipoRecurso1
    template_name = 'recurso_pr/listar_tipo_recurso_pr.html'


'''Modificar Tipo de Recurso '''


class TipoRecursoModificar(UpdateView):
    """Modificar Tipo de Recurso utilizando view UpdateView
    Modelo utilizado de TipodeRecurso1
    Formulario utilizado con datos de nombre_recurso y indicardor de recursos reservable
    Template de modificar_tipo_recurso_pr.html
    Redireccionamiento despues de guardar el registro a Listar Tipo de Recurso"""
    model = TipoRecurso1
    form_class = TipoRecursoForm2
    template_name = 'recurso_pr/modificar_tipo_recurso_pr.html'
    success_url = reverse_lazy('recurso_pr:recurso_pr_listar_tipo')

'''Funcion para Buscar Recursos '''


def buscar_recurso(request):
    """ Busqueda de Recurso utilizando filtros, en este caso, el nombre del tipo de recurso.
        Modelo utilizado de Recurso1
        q: variable que contendra el patron de busqueda
        recursos: variable que contendra todos los registros que contengan alguna coincidencia
        con el dato guardado en q.
        Los registros encontrados en la busquda se desplegaran en forma de lista en el template
        recurso_pr_detalle.html.
        La busqueda podra iniciarse desde el template de Listar del Menu Recursos, listar_precurso.html
        """
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            recursos = Recurso1.objects.filter(tipo_id__nombre_recurso__icontains=q)
            return render(request, 'recurso_pr/recurso_pr_detalle.html', {'recursos': recursos, 'query': q})
    return render(request, 'recurso_pr/listar_recurso.html', {'error': error})


'''Funcion para Buscar Tipo de Recursos '''


def buscar_tipo_recurso(request):
    """ Busqueda del Tipo de Recurso utilizando filtros, en este caso, el nombre del tipo de recurso.
           Modelo utilizado de TipodeRecurso1
           q: variable que contendra el patron de busqueda
           recursos: variable que contendra todos los registros que contengan alguna coincidencia
           con el dato guardado en q.
           Los registros encontrados en la busquda se desplegaran en forma de lista en el template
           recurso_pr_detalle_tipo.html.
           La busqueda podra iniciarse desde el template de Listar del Menu Recursos, listar_tipo_precurso_pr.html
           """
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            recursos = TipoRecurso1.objects.filter(nombre_recurso__icontains=q)
            return render(request, 'recurso_pr/recurso_pr_detalle_tipo.html', {'recursos': recursos, 'query': q})
    return render(request, 'recurso_pr/listar_tipo_recurso_pr.html', {'error': error})

'''Lista de Recursos con el uso del view ListView'''


class ListadoRecurso(ListView):
    """ Modelo utilizado de Recurso1
    template listar_recurso.html
    Paginacion de 10 registros"""
    model = Recurso1
    template_name = 'recurso_pr/listar_recurso.html'


'''Modificar Recurso existente con el uso del view UpdateView'''


class RecursoModificar(UpdateView):
    """Modelo utilizado de Recurso1
    Formulario con contenido de tipo_id y estado del recurso
    Template a utilizar para realizar las modificaicones: modificar_recurso.html
    Redireccionar a la lista de Recursos Existentes: listar_recurso.html con nombre recurso_pr_listar"""
    model = Recurso1
    form_class = RecursoForm
    template_name = 'recurso_pr/modificar_recurso.html'
    success_url = reverse_lazy('recurso_pr:recurso_pr_listar')


def recurso_edit(request, recurso_id):
    """Modelo utilizado de Recurso1
        En la variable recurso se guarda el registro con recurso_id igual al parametro recibido.
        form: es el formulario que mostrara todos los datos del recurso en pantalla.
        En caso de ser un Metodo Get:
        Se validara el formulario, luego, si el formulario es valido, se guardaran los datos del
        formulario form en la base de datos.

        Template a utilizar para realizar las modificaicones: modificar_recurso.html
        Redireccionar a la lista de Recursos Existentes: listar_recurso.html con nombre recurso_pr_listar"""
    recurso = Recurso1.objects.get(recurso_id=recurso_id)
    if request.method == 'GET':
        form = RecursoForm(instance=recurso)
    else:
        form = RecursoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
        return redirect('recurso_pr:recurso_pr_listar')
    return render(request, 'recurso_pr/modificar_recurso.html', {'form': form})


'''Lista todas las caracteristicas que pertenecen a un Recurso'''


def lista_caracteristica(request, recurso_id):
    """Se recuperan las caracteristicas del recurso con id recurso_id y se guarda en la variable
    caracteristica.
    contexto = envia al template los objetos que debe desplegar en la lista de Caracteristicas
    Se redirecciona al template lista_caracteristica.html"""
    caracteristica = DescripCarac.objects.filter(recurso__recurso_id=recurso_id)
    contexto = {'caracteristica': caracteristica}
    return render(request, 'recurso_pr/lista_caracteristica.html', contexto)


'''Modificar Caracteristicas pertenecientes al Recurso'''


def modificar_caracteristicas(request, ctra_id):
    """Parametro ctra_id trae el id de la caracteristica a modificar
        caracteristeca = se recuperan los datos del objeto con id ctra_id
        Si el metodo corresponde a un Get, se muestran los datos de dicha caracteristica
        Si el metodo es Post, se guardan los datos modificados de la caracteristica
        Se valida el formulario y se guardan los cambios
        Se redirecciona a la Lista de Recursos"""
    caracteristica = Caracteristica.objects.get(ctra_id=ctra_id)
    if request.method == 'GET':
        form = CaracteristicaForm(instance=caracteristica)
    else:
        form = CaracteristicaForm(request.POST, instance=caracteristica)
        if form.is_valid():
            form.save()
        return redirect('recurso_pr:recurso_pr_listar')
    return render(request, 'recurso_pr/modificar_caracteristicas.html', {'form': form})

