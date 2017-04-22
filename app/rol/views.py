
from django.shortcuts import render, redirect
from django.http import  HttpResponse
from app.rol.forms import RolForm
from app.rol.models import Rolusuario
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from app.usuario.models import UsuarioUser
from app.rol.forms import AsignarRolForm
# Create your views here.

''' Funciones referentes al Rol, crear, modificar, eliminar, listar, asignar y desasignar rol a un usuario'''


def rol_crear(request):
    """Si se reciben datos sera el metodo Post, por lo que se guardara el nuevo registro de rol
        crear_form: es la variable donde se guardan los datos enviados por el cliente a traves del formulario.
        RolForm: es el formulario en donde se cargan los datos en el template crear_rol.html
        crear_rol.html: es el template donde se crea el nuevo rol
        rol_listar.html: es el template donde se redirecciona, despues de concretarse una accion.
    """
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
    """ Funcion que Lista todos los registros creados del modelo Rolusuario y los envia al template listar_rol.html"""
    qroles = Rolusuario.objects.all().order_by('id')
    contexto = {'roles': qroles}
    return render(request, 'listar_rol.html', contexto)


# vista basada en clases
class ListarRol (ListView):
    """Clase para crear el Listado de los roles, se indica el modelo y el template que lo contendra"""
    # Se indica el modelo Rolusuario
    model = Rolusuario
    template_name = 'listar_rol.html'

# Vista de modificar rol


def modificar_rol(request, id_rol):
    """ Modifica los campos de un registro existente de Rol
        dato: variable que indica una inexistencia del id proporcionado por el cliente
        rol_modificar: variable que guarda todos los datos existentes del registro indicado con el id del rol
        Si es un metodo Get:
            crear_form: en esta variable se guardan lds datos no modificados.
        Si es un metodo Post:
            crear_form: guarda los datos modificados en esta variable y se guardan finalmente.
        """
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
    """Elimina el registro del rol indicado con el id del rol"""
    dato = get_object_or_404(Rolusuario, pk=id_rol)
    try:
        rol_eliminar = Rolusuario.objects.get(id=id_rol)
        if request.method == 'POST':
            rol_eliminar.delete()
            return redirect('rol:rol_listar')
        return render(request, 'eliminar_rol.html', {'crear_form': rol_eliminar})
    except (KeyError, NotImplementedError):
        return render(request, 'listar_rol.html', {'error': dato, 'error_message': "El registro no existe.", })


def mod_rol(request):
    return render(request, 'mod_rol.html')


def rol_asignar(request):
    mensaje = None
    if request.method == 'POST':
        cedula = request.POST['cedula']
        nuevo_rol = request.POST['rol']
        if UsuarioUser.objects.filter(cedula=cedula):
            user = UsuarioUser.objects.get(cedula=cedula)
            user.rol = nuevo_rol
            user.save()
            mensaje = "Rol Asignado"
        else:
            mensaje = "No es un Usuario valido"
        form = AsignarRolForm
        context = {
            'mensaje':mensaje,
            'form':form,
        }
        return render(request,'asignar_rol.html',context)
    else:
        form = AsignarRolForm
        context = {
            'mensaje': mensaje,
            'form': form,
        }
    return render(request, 'asignar_rol.html', context)
