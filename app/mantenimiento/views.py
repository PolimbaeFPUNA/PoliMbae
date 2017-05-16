''' Funciones para el manejo del modulo de mantenimiento de recursos'''
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from app.mantenimiento.models import Mantenimiento
from app.mantenimiento.forms import *
from django.core.urlresolvers import reverse_lazy
from app.recurso_pr.models import *
from django.utils.dateparse import parse_date, parse_time
from app.reserva.models import *
from django.core.mail import send_mail, send_mass_mail

def listar_mantenimiento(request):
    """ La vista listar_mantenimiento, despliega todos los registros de mantenimiento
     creados sobre los recursos ordenados por id del registro, proporciona las operaciones de: modificar y eliminar
     para cada uno"""
    mant= Mantenimiento.objects.all().order_by('id')

    return render(request, "mantenimiento/listar_mantenimiento.html", {"mant":mant})


def crear_mantenimiento(request):
    """ La vista despliega el formulario para crear un nuevo registro de mantenimiento sobre algun recurso
    con las siguientes condiciones: previa verificacion de fechas y horas de entrega y finalizacion,
    previa verificacion de solapamiento entre registros de mantenimiento sobre el recurso
    y previa verificacion de solapamiento con reservas sobre el recurso
    """
    rform= None
    mensaje= None
    if request.method == 'POST':
        form= MantForm(request.POST)

        if request.POST.get('listar'):
            rform=ListRecursoForm(tipo=request.POST['tipo_recurso'])

        if request.POST.get('guardar'):
            fecha_entrega= request.POST['fecha_entrega']
            fecha_fin= request.POST['fecha_fin']
            hora_entrega= request.POST['hora_entrega']
            hora_fin= request.POST['hora_fin']
            recurso = Recurso1.objects.get(recurso_id=request.POST['lista'])
            rtipo = TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])
            if verificar_hora_fecha(fecha_entrega, fecha_fin, hora_entrega, hora_fin):
                mensaje = "Verifique fechas y horas"
            if verificar_mantenimiento_crear(recurso,fecha_entrega, fecha_fin):
                if not mensaje:
                    mensaje = "Este recurso tiene agendado mantenimiento en el rango de fechas escogidas"
                else:
                    mensaje += "-Este recurso tiene agendado mantenimiento en el rango de fechas escogidas"
            if not mensaje:
                Mantenimiento.objects.create(tipo_recurso=rtipo,recurso=recurso,
                                         fecha_entrega=request.POST['fecha_entrega'], fecha_fin=request.POST['fecha_fin'],
                                         tipo= request.POST['tipo'], hora_entrega=request.POST['hora_entrega'],
                                             hora_fin=request.POST['hora_fin'])
                verificar_reservas(fecha_entrega,fecha_fin, hora_entrega, hora_fin, recurso)

                return redirect("mantenimiento:mantenimiento_listar")

    else:
        form= MantForm()
        rform=ListRecursoForm(tipo=-1)

    context ={'form':form, 'rform':rform, 'mensaje':mensaje}
    return render(request, 'mantenimiento/crear_mantenimiento.html', context)


def modificar_mantenimiento(request, pk):
    """ La vista despliega el formulario para modificar un registro de mantenimiento sobre algun recurso
        con las siguientes condiciones: previa verificacion de fechas y horas de entrega y finalizacion,
        previa verificacion de solapamiento entre registros de mantenimiento sobre el recurso
        y previa verificacion de solapamiento con reservas sobre el recurso
        """
    mensaje= None
    mant= Mantenimiento.objects.get(pk=pk)
    list_tipo= TipoRecurso1.objects.all()
    list_recurso= Recurso1.objects.filter(tipo_id=mant.tipo_recurso)
    form = ChoiceForm(instance=mant)
    if request.method == 'POST':
        if request.POST.get('guardar'):
            tipo_recurso= TipoRecurso1.objects.get(nombre_recurso=request.POST.get('tipo_recurso'))
            recurso= Recurso1.objects.get(recurso_id=request.POST.get('recurso'))
            fecha_entrega= request.POST.get('fecha_entrega')
            fecha_fin= request.POST.get('fecha_fin')
            hora_entrega= request.POST.get('hora_entrega')
            hora_fin = request.POST.get('hora_fin')
            tipo= request.POST.get('tipo')
            if verificar_hora_fecha(fecha_entrega,fecha_fin, hora_entrega, hora_fin):
                mensaje= "Fechas y horas incorrectas"
            if verificar_mantenimiento_modif(recurso,fecha_entrega,fecha_fin,mant.id):
                if not mensaje:
                     mensaje = "Este recurso tiene agendado mantenimiento en el rango de fechas escogidas"
                else:
                     mensaje += "-Este recurso tiene agendado mantenimiento en el rango de fechas escogidas"

            if not mensaje:
                mant.tipo_recurso = tipo_recurso
                mant.recurso = recurso
                mant.fecha_entrega = fecha_entrega
                mant.fecha_fin = fecha_fin
                mant.tipo= tipo
                mant.hora_entrega= hora_entrega
                mant.hora_fin= hora_fin
                mant.save()
                verificar_reservas(fecha_entrega, fecha_fin, hora_entrega, hora_fin, recurso)
                return redirect("mantenimiento:mantenimiento_listar")
    context = {'mant': mant, 'list': list_tipo, 'rlist': list_recurso, 'form':form, 'mensaje': mensaje}
    return render(request, 'mantenimiento/modificar_mantenimiento.html',context )

class EliminarMant(DeleteView):
    """ Elimina un registro de mantenimiento """
    model= Mantenimiento
    template_name= "mantenimiento/eliminar_mantenimiento.html"
    success_url = reverse_lazy("mantenimiento:mantenimiento_listar")

def verificar_hora_fecha(fecha_entrega, fecha_fin, hora_entrega, hora_fin):
    """ Funcion que sirve para verificar si se ha ingresado una hora de entrega mayor a la hora de finalizacion y
con fechasde entrega y finalizacion iguales, o si la fecha de entrega es mayor que la fecha de finalizacion"""
    f1= fecha_entrega
    f2 = fecha_fin
    h1= parse_time(hora_entrega)
    h2= parse_time(hora_fin)

    if f2==f1 and h2 <= h1:
        return True
    elif f2 < f1:
        return True
    else:
        return False



def verificar_reservas(fecha_entrega, fecha_fin, hora_entrega, hora_fin,recurso):
    """Funcion que verifica las reservas programadas en el rango de fechas y horas en el que se agendara el mantenimiento.
    Si existen reservas coincidentes con el mantenimiento que se agendara, se reasigna otro recurso a la reserva"""
    f1 = parse_date(fecha_entrega)
    f2 = parse_date(fecha_fin)
    h1 = parse_time(hora_entrega)
    h2= parse_time(hora_fin)
    reserva= ReservaGeneral.objects.filter(recurso=recurso.recurso_id)
    for r in reserva:
            if r.fecha_reserva == f1 and r.fecha_reserva == f2:
                if h1 <= r.hora_inicio and h2 >= r.hora_inicio:
                    reasignar_recurso_reserva(recurso,r)
                elif h1 > r.hora_inicio and h1 < r.hora_fin:
                    reasignar_recurso_reserva(recurso, r)
                elif h1 == r.hora_inicio:
                    reasignar_recurso_reserva(recurso,r)
            elif f1==r.fecha_reserva:
                if r.hora_fin > h1:
                    reasignar_recurso_reserva(recurso,r)
            elif f2 == r.fecha_reserva:
                if r.hora_inicio < h2:
                    reasignar_recurso_reserva(recurso,r)
            elif f1< r.fecha_reserva and r.fecha_reserva < f2:
                reasignar_recurso_reserva(recurso,r)
            else:
                print ('do nothing')




def reasignar_recurso_reserva (recurso, reserva):
    """ La funcion se encarga de reasignar un recurso del mismo tipo a una reserva cuya rango de hora fecha coincide con
     el registro de mantenimiento que se desea agendar. Primeramente se buscan aquellos recursos que se encuentren libres de
     reservas y mantenimientos, sino, se realiza la busqueda sobre aquellos que tienen reservas pero no coincidentes
     con el rango de la reserva que se desea reasignar, por ultimo, si no se encuentra ningun recurso del tipo buscado, se
     cancela la reserva y se notifica al usuario via e-mail"""
    tipo = recurso.tipo_id
    recurso_listar= Recurso1.objects.filter(tipo_id=tipo)
    flag= None
    x=None
    for r in recurso_listar:
        flag = None
        if buscar_recurso_lista_reservas(r,tipo) and buscar_recurso_lista_mantenimiento(r, reserva):
            reserva.recurso = r
            reserva.save()
            break
        if r.recurso_id != recurso.recurso_id and buscar_recurso_lista_mantenimiento(r, reserva):
            reserva_lista= ReservaGeneral.objects.filter(recurso=r.recurso_id)
            for e in reserva_lista:
                aux= Recurso1.objects.get(recurso_id=e.recurso.recurso_id)
                print(aux.recurso_id)
                if (tipo==aux.tipo_id):
                        if reserva.fecha_reserva == e.fecha_reserva:
                            if reserva.hora_inicio <= e.hora_inicio and e.hora_inicio <= reserva.hora_fin:
                                flag=1
                            elif reserva.hora_inicio > e.hora_inicio and e.hora_fin > reserva.hora_inicio:
                                flag=1
        else:
            flag=1
        if not flag:
            print(r.recurso_id)
            reserva.recurso = r
            reserva.save()
            break
    if flag:
        fecha= reserva.fecha_reserva.strftime('%Y-%m-%d')
        hora_i= reserva.hora_inicio.strftime('%H:%M')
        hora_f= reserva.hora_fin.strftime('%H:%M')
        email= reserva.profile.user.email
        send_mail(
            'Reserva Cancelada en Polimbae',
            'La reserva solicitada para el dia: '+fecha+' y hora: '+hora_i+'-'+hora_f+ ' ha sido cancelada por falta de disponibilidad del tipo de recurso solicitado',
            'polimbae@gmail.com',
            [email],
            fail_silently=False,
        )
        borrar_reserva(reserva)





def buscar_recurso_lista_reservas(recurso, tipo):
    """Funcion auxiliar para buscar si un recurso se encuentra completamente libre de reservas
    y poder asignar el primero que se encuentra"""

    lista= ReservaGeneral.objects.filter(recurso=recurso.recurso_id)
    flag= None
    for r in lista:
        aux= Recurso1.objects.get(recurso_id= r.recurso.recurso_id)
        if aux.tipo_id==tipo:
            if(recurso.recurso_id==aux.recurso_id):
                flag= 1
                break
    if not flag:
        return  True
    else:
        return False



def buscar_recurso_lista_mantenimiento(recurso, reserva):
    """Funcion auxiliar que busca si un recurso que no esta
    en la lista de reservas, esta en la lista de mantenimiento para la fecha requerida
    y luego impide que el mismo sea utilizado para ragendar """
    lista = Mantenimiento.objects.filter(recurso=recurso.recurso_id)
    flag= None
    for m in lista:
        if m.tipo_recurso == recurso.tipo_id:
            if m.recurso.recurso_id == recurso.recurso_id:
                if m.fecha_entrega >= reserva.fecha_reserva <= m.fecha_fin:
                    flag=1
                    break
    if not flag:
        return  True
    else:
        return False

def verificar_mantenimiento_crear(recurso, fecha1, fecha2):
    """Al crear un registro de mantenimiento, esta funcion  controla que no se solapen los registros de manteniminentos sobre el recurso """
    f1= parse_date(fecha1)
    f2= parse_date(fecha2)
    flag= None
    lista= Mantenimiento.objects.filter(recurso=recurso.recurso_id)
    for m in lista:
        if m.fecha_entrega == f1:
            flag= 1
            break
        elif m.fecha_entrega < f1 and f1 < m.fecha_fin:
            flag=1
            break
        elif m.fecha_entrega > f1 and f2 >= m.fecha_entrega:
            flag=1
            break
        elif m.fecha_fin== f1:
            flag=1
            break
    if flag:
        return True
    else:
        return False


def verificar_mantenimiento_modif(recurso, fecha1, fecha2, mant_id):
    """ Al modificar un registro de mantenimiento, esta funcion controla que no se solape con otros registros de mantenimiento sobre el recurso,
    pero sin evaluar el registro de mantenimiento actual """
    f1= parse_date(fecha1)
    f2= parse_date(fecha2)
    flag= None
    lista= Mantenimiento.objects.filter(recurso=recurso.recurso_id)

    for m in lista:
        if m.id != mant_id:
            if m.fecha_entrega == f1:
                flag= 1
                break
            elif m.fecha_entrega < f1 and f1 < m.fecha_fin:
                flag=1
                break
            elif m.fecha_entrega > f1 and f2 >= m.fecha_entrega:
                flag=1
                break
            elif m.fecha_fin== f1:
                flag=1
                break
    if flag:
        return True
    else:
        return False

def borrar_reserva (reserva):
    reserva_delete= ReservaGeneral.objects.filter(reserva_id=reserva.reserva_id)
    reserva_delete.delete()

def buscar(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            mant = Mantenimiento.objects.filter(tipo_recurso__nombre_recurso__icontains=q)
            return render(request, 'mantenimiento/consultar_mantenimiento.html', {'mant': mant, 'query': q})
    return render(request, 'mantenimiento/consultar_mantenimiento.html', {'error': error})

def crear_mant_preventivo(request):

    if request.method == 'POST':
        clas=0
