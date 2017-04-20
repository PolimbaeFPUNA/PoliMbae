from django.shortcuts import render, redirect
from django.http import  HttpResponse
from app.rol.forms import RolForm
from app.rol.models import Rolusuario
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView

# Create your views here.


def rol_crear(request):
    if request.method == 'POST':
        crear_form = RolForm(request.POST)
        # se validan los datos recibidos del post en la variable
        if crear_form.is_valid():
            crear_form.save()  # se guardan los datos del formulario
        return redirect('rol:rol_listar')
    else:
        crear_form = RolForm()
    # se coloca el nombre del template y el archivo de html donde esta el formulario y el contexto del formulario
    return render(request, 'crear_rol.html', {'crear_form': crear_form})

# vista basada en funciones
def rol_listar(request):
    qroles = Rolusuario.objects.all().order_by('id')
    contexto = {'roles': qroles}
    return render(request, 'listar_rol.html', contexto)


# vista basada en clases
class ListarRol (ListView):
    # Se indica el modelo Rolusuario
    model = Rolusuario
    template_name = 'listar_rol.html'

# Vista de modificar rol


def modificar_rol(request, id_rol):
    dato = get_object_or_404(Rolusuario, pk=id_rol)
    try:
        rol_modificar = Rolusuario.objects.get(id=id_rol)
        if request.method == 'GET':
            crear_form = RolForm(instance=rol_modificar)
        else:
            crear_form = RolForm(request.POST, instance=rol_modificar)
            if crear_form.is_valid():
                crear_form.save()
                return redirect('rol:rol_listar')
        return render(request, 'modificar_rol.html', {'crear_form': crear_form})
    except (KeyError, NotImplementedError):
        return render(request, 'listar_rol.html', {'error': dato, 'error_message': "El registro no existe.", })


def eliminar_rol(request, id_rol):
    dato = get_object_or_404(Rolusuario, pk=id_rol)
    try:
        rol_eliminar = Rolusuario.objects.get(id=id_rol)
        if request.method == 'POST':
            rol_eliminar.delete()
            return redirect('rol:rol_listar')
        return render(request, 'eliminar_rol.html', {'crear_form': rol_eliminar})
    except (KeyError, NotImplementedError):
        return render(request, 'listar_rol.html', {'error': dato, 'error_message': "El registro no existe.", })




