# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from app.reserva_new.models import Solicitud, Reserva
from app.recurso_pr.models import Recurso1, TipoRecurso1
from app.reserva_new.forms import *
from app.usuario.models import Profile
from app.log.models import *
from django.utils.dateparse import parse_date, parse_time
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Q
from datetime import datetime,timedelta, date
import time
# Create your views here.

def crear_solicitud(request):
    """ Se obtienen los datos ingresados para:
    1- Creacion de Reservas directas (fecha igual a la de hoy)
    2- Creacion de Solicitud de Reserva de un Recurso Especifico
    3- Creacion de Soliciutd de Reserva de un Recurso General
    Las verificaciones que se realizan:
    1- Hora de inicio y fin iguales
    2- Hora de fin mayor a la hora de inicio
    3- Busqueda de Recursos disponibles para Solicitudes Generales
    4- Aprobacion y Rechazo de Reservas Directas en caso de no disponibilidad
    5- Todas las solicitudes de Reservas son aceptadas y entran en competencia
    """
    mensaje = None
    if request.method == 'POST':
        form= SolicitudForm(initial={'tipo_recurso':request.POST.get('tipo_recurso'), 'fecha_reserva':request.POST.get('fecha_reserva'),'hora_inicio': request.POST.get('hora_inicio'),'hora_fin':request.POST.get('hora_fin')})
    else:
        form = SolicitudForm()
    form.fields['tipo_recurso'].widget.attrs['onChange'] = 'document.getElementById("get_datos").click();'
    if request.POST.get('tipo_recurso') != '':
        form.fields['recurso'].queryset = Recurso1.objects.filter(tipo_id=request.POST.get('tipo_recurso')).exclude(estado='EM')
    else:
        form.fields['recurso'].queryset = Recurso1.objects.none()


    recurso_id=None
    if request.method == 'POST' and request.POST.get('guardar'):

        hoy = date.today()
        if not request.POST.get('tipo_recurso'):
            mensaje= "Debe seleccionar el tipo de recurso"
        elif not request.POST.get('fecha_reserva'):
            mensaje= "Debe seleccionar la fecha"
        elif not request.POST.get('hora_inicio'):
            mensaje= "Debe seleccionar la hora de inicio"
        elif not request.POST.get('hora_fin'):
            mensaje= "Debe seleccionar la hora de finalizacion"
        elif parse_date(request.POST.get('fecha_reserva'))< hoy:
            mensaje="La fecha seleccionada es menor que la actual. "
        elif hoy + timedelta(days=1) == parse_date(request.POST.get('fecha_reserva')):
            mensaje="Las reservas anticipadas se realizan hasta dos dias antes, usted eligio la fecha de mañana. "
        elif parse_date(request.POST.get('fecha_reserva'))== hoy and parse_time(request.POST.get('hora_inicio')) < datetime.now().time():
            mensaje = "La hora de inicio es menor que la hora actual. "
        elif parse_time(request.POST.get('hora_fin')) < parse_time(request.POST.get('hora_inicio')):
            mensaje = "La hora de finalizacion es menor que la hora de inicio. "
        elif request.POST.get('hora_inicio') == request.POST.get('hora_fin'):
            mensaje= "La hora de finalizacion es igual a la hora de inicio. "
        else:
            usuario= Profile.objects.get(user__username=request.POST['profile'])
            fecha= request.POST['fecha_reserva']
            hora_inicio= request.POST['hora_inicio']
            hora_fin= request.POST['hora_fin']
            f= parse_date(fecha)
            tipo = TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])
            if request.POST['recurso'] == '' and f != hoy:
                recurso= buscar_recurso_disponible(fecha, hora_inicio, hora_fin, tipo)
                s =Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                         usuario=usuario, recurso=recurso, estado='PEN')
                Log.objects.create(usuario=request.user, fecha_hora=datetime.now(),
                                   mensaje='Crear Solicitud ' + s.__str__())

                return redirect("reserva_new:listar_reservas_user")
            elif f == hoy and request.POST['recurso'] == '':
                recurso= verificar_reserva(fecha, hora_inicio, hora_fin, tipo)

                if recurso:
                    r = Reserva.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                           usuario=usuario, recurso_reservado=recurso,estado_reserva='CONFIRMADA')
                    Log.objects.create(usuario=request.user, fecha_hora=datetime.now(),
                                       mensaje='Crear Reserva ' + r.__str__())
                    return redirect("reserva_new:listar_reservas_user")

                else:
                    mensaje= "No hay recursos disponibles para fecha y rango de horas solicitada"
            elif f == hoy and request.POST['recurso'] != '':
                recurso= Recurso1.objects.get(recurso_id=request.POST['recurso'])
                if verificar_reserva_recurso(fecha, hora_inicio, hora_fin, tipo,recurso):
                    r =Reserva.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                           usuario=usuario, recurso_reservado=recurso, estado_reserva='CONFIRMADA')
                    Log.objects.create(usuario=request.user, fecha_hora=datetime.now(),
                                       mensaje='Crear Reserva ' + r.__str__())
                    return redirect("reserva_new:listar_reservas_user")
                else:
                    mensaje = "El recurso no esta disponible en fecha y rango de horas solicitada"

            else:
                recurso= Recurso1.objects.get(recurso_id=request.POST['recurso'])
                s=Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                         usuario=usuario, recurso=recurso, estado='PEN')
                Log.objects.create(usuario=request.user, fecha_hora=datetime.now(),
                                   mensaje='Crear Solicitud ' + s.__str__())
                return redirect("reserva_new:listar_reservas_user")

    return render(request, "reserva_new/crear_solicitud1.html", {'form':form, 'mensaje': mensaje})

def modificar_reserva(request, idres):
    """ La vista permite:
    1- Modificar el usuario, si el administrador necesita hacer la reserva en favor de alguien
    2- Modificar el recurso. Ya que a la hora de la entrega el que se ha a asignado podria no estar disponible
    ya sea porque paso a mantenimiento o porque aun no se ha devuleto """
    r= Reserva.objects.get(pk=idres)
    tipo = r.recurso_reservado.tipo_id.nombre_recurso
    form = ReservaModform(instance=r)
    horaIreal = (datetime.combine(r.fecha_reserva, r.hora_inicio) - timedelta(
        minutes=15)).time()
    horaFreal = (datetime.combine(r.fecha_reserva, r.hora_fin) + timedelta(
        minutes=15)).time()
    recursos1 = Recurso1.objects.filter(Q(tipo_id=r.recurso_reservado.tipo_id), Q(estado='DI') | Q(estado='EU'))
    recursos2 = Recurso1.objects.filter(Q(tipo_id=r.recurso_reservado.tipo_id),
                                        Q(reserva__fecha_reserva=r.fecha_reserva,
                                          reserva__hora_inicio__range=[horaIreal, horaFreal],
                                          reserva__estado_reserva='CONFIRMADA')
                                        | Q(reserva__fecha_reserva=r.fecha_reserva,
                                            reserva__hora_fin__range=[horaIreal, horaFreal],
                                            reserva__estado_reserva='CONFIRMADA')).exclude(pk=r.recurso_reservado.pk)
    # recursos libres para el horario
    recursos = recursos1.exclude(pk__in=recursos2.all().values_list('pk', flat=True))
    form.fields['recurso_reservado'].queryset = recursos
    if request.method == 'POST':

        form = ReservaModform(request.POST,instance=r)

        form.fields['recurso_reservado'].queryset = recursos
        tipo = r.recurso_reservado.tipo_id.nombre_recurso

        if form.is_valid():
            r=form.save()
            Log.objects.create(usuario=request.user,fecha_hora=datetime.now(),mensaje='Modifica Reserva '+r.__str__())
            return redirect("reserva_new:reserva_listar")
        else:
            print 'invalid'
            print request.POST

    return render(request,'reserva_new/modificar_reserva.html', {'tipo':tipo, 'form':form})



def verificar_reserva_recurso(fecha, hora_inicio, hora_fin, tipo,recurso):
    """ La funcion se ocupa de verificar si sobre el recursos especifico elegido en la Reserva Directa
    existe alguna reserva que coincida en fecha y rango de horas elegidas o con menos de 15 minutos entre horas de inicio
    y fin de diferencia.
    1- Retorna un valor Falso si se ha encontrado una reserva coincidente en fecha y rango de horas sobre ese recurso solicitado
    2- Retorna un valor de Verdadero si el recurso seleccionado no posee reservas coincidentes en la fecha y rango de horas escogidos. """
    r = None
    f = parse_date(fecha)
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    h2_aux = (datetime.combine(date.today(), h2) + timedelta(minutes=15)).time()
    h1_aux = (datetime.combine(date.today(), h1) - timedelta(minutes=15)).time()
    lista_reserva = Reserva.objects.all()

    for r in lista_reserva:
        if recurso.recurso_id == r.recurso_reservado.recurso_id and r.estado_reserva != 'FINALIZADA' and r.estado_reserva != 'CANCELADA':
            if r.fecha_reserva == f:

                if r.hora_inicio >= h1 and r.hora_inicio < h2:
                   return False

                elif r.hora_fin > h1 and r.hora_fin < h2:
                    return False

                elif r.hora_inicio <= h1 and r.hora_fin >= h2:
                    return False
                elif h2_aux > r.hora_inicio and h1 < r.hora_inicio:
                    return False
                elif h1_aux < r.hora_fin and r.hora_inicio < h1:
                    return False

    return True
def verificar_reserva(fecha, hora_inicio, hora_fin, tipo):
    """ La funcion se encarga de verificar si hay recursos sin reservas del tipo solicitado para la fecha y el rango de horas
    seleccionado por el usaurio.
    1- Si no hay disponibles retorna un objeto null, que se reenvia a la funcion de crear para luego informarselo
    al usuario en el formulario.
    2- Si se consiguio un recurso disponible, se renderiza a la lista de reservas y solicitudes del usuario """
    f = parse_date(fecha)
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    h2_aux = (datetime.combine(date.today(), h2) + timedelta(minutes=15)).time()
    h1_aux = (datetime.combine(date.today(), h1) - timedelta(minutes=15)).time()
    lista_reserva= Reserva.objects.all()
    lista_recurso = Recurso1.objects.filter(tipo_id=tipo.tipo_id, estado__in=['EU','DI'])
    for recurso in lista_recurso:
        count=0
        flag=None
        for r in lista_reserva:
            if recurso.recurso_id == r.recurso_reservado.recurso_id and r.estado_reserva != 'FINALIZADA' and r.estado_reserva != 'CANCELADA':
                if r.fecha_reserva == f:
                    flag = 1
                    if r.hora_inicio >= h1 and r.hora_inicio < h2:
                        count=count+1

                    elif r.hora_fin > h1 and r.hora_fin < h2:
                        count=count+1

                    elif r.hora_inicio <= h1 and r.hora_fin >= h2:
                        count=count+1
                    elif h2_aux > r.hora_inicio and h1 < r.hora_inicio:
                        count = count + 1
                    elif h1_aux < r.hora_fin and r.hora_inicio < h1:
                        count = count + 1
        if flag==1:
            if count==0:
                return recurso
        else:
            return recurso
    return None

def buscar_recurso_disponible(fecha, hora_inicio,hora_fin, tipo):
    """La funcion auxiliar busca el recurso que menos solicitudes tiene para asignarle a la nueva solicitud,
    asi el usuario tiene menos competidores.
    1- Retorna el recurso con menos solicitudes en todos los casos"""
    r=None
    f= parse_date(fecha)
    h1= parse_time(hora_inicio)
    h2= parse_time(hora_fin)
    count= 0
    previo=99999
    lista_solicitud= Solicitud.objects.filter(Q(recurso__tipo_id= tipo.tipo_id) | Q(estado='PEN'))
    lista_recurso= Recurso1.objects.filter(tipo_id=tipo.tipo_id)

    for recurso in lista_recurso:
        count=0
        flag=None
        for s in lista_solicitud:
            if s.recurso == recurso:

                if s.fecha_reserva == f:
                    flag = 1
                    if s.hora_inicio >= h1 and s.hora_inicio < h2:
                        count=count+1

                    elif s.hora_fin > h1 and s.hora_fin < h2:
                        count=count+1

                    elif s.hora_inicio <= h1 and s.hora_fin >= h2:
                        count=count+1
        if flag==1:
            if count==0:
                return recurso
            elif count <= previo:
                previo=count
                r= recurso
        else:
            return recurso
    return r

def confirmar_solicitud(request, idsol):
    """ La funcion controla el boton de Confirmar dentro de la lista de solicitudes.
    Se selecciona manualmente a criterio del administrador la solicitud que se confirmara
    Al confirmarse una solicitud sobre un recurso, se eliminan todas las solicitudes que solapen en fecha y rango
    de horas con la que se esta confirmando.
    Se crea una nueva reserva, asignando el recurso como reservado, y la misma pasa al estado de Confirmada.
    La solicitud confirmada tambien se elimina, porque la misma paso a convertirse en Reserva"""
    solicitud= Solicitud.objects.get(solicitud_id=idsol)

    form= SolicitudConfirmForm(instance=solicitud)

    if request.method == 'POST':

            Reserva.objects.create(usuario=solicitud.usuario, recurso_reservado=solicitud.recurso, fecha_reserva=solicitud.fecha_reserva,
                                    hora_inicio=solicitud.hora_inicio, hora_fin=solicitud.hora_fin, estado_reserva='CONFIRMADA')
            notificar_confirmacion(solicitud)
            rechazar_colisionadas(solicitud)
            solicitud.delete()
            return redirect("reserva_new:solicitud_listar")

    return render(request, "reserva_new/confirmar_solicitud.html",{'form':form, 'solicitud':solicitud})

def rechazar_colisionadas(solicitud):
    """ La funcion auxiliar se ocupa de buscar todas las solicitudes que coisionan en fecha y rango de horas con
    la solicitud que se eligio confirmar. Las encuentra y las elimina. """
    f= solicitud.fecha_reserva
    h1= solicitud.hora_inicio
    h2= solicitud.hora_fin
    h2_aux= (datetime.combine(date.today(), solicitud.hora_fin) + timedelta(minutes=15)).time()
    h1_aux= (datetime.combine(date.today(), solicitud.hora_inicio) - timedelta(minutes=15)).time()
    lista_solicitud= Solicitud.objects.filter(recurso=solicitud.recurso)

    for s in lista_solicitud:
        if s.fecha_reserva == f and s.solicitud_id != solicitud.solicitud_id:
            if s.hora_inicio >= h1 and s.hora_inicio < h2:
                notificar_rechazo(s)
                s.estado='RCH'
                s.save()
            elif s.hora_fin > h1 and s.hora_fin < h2:
                notificar_rechazo(s)
                s.estado = 'RCH'
                s.save()
            elif s.hora_inicio  <= h1 and s.hora_fin >= h2:
                notificar_rechazo(s)
                s.estado = 'RCH'
                s.save()
            elif h2_aux > s.hora_inicio and h1 < s.hora_inicio:
                notificar_rechazo(s)
                s.estado = 'RCH'
                s.save()
            elif h1_aux < s.hora_fin and s.hora_inicio < h1:
                notificar_rechazo(s)
                s.estado = 'RCH'
                s.save()
def eliminar_solicitud(request, idsol):
    """ La funcion controla el boton de Cancelar en la lista Mis Reservas y Solicitudes, donde se listan las que pertenecen al
     usuario logueado actualmente"""
    solicitud= Solicitud.objects.get(solicitud_id=idsol)
    form= SolicitudConfirmForm(instance=solicitud)
    if request.method == 'POST':
        solicitud.estado = 'RCH'
        solicitud.save()
        return redirect('reserva_new:solicitud_listar')
    return render(request,'reserva_new/eliminar_solicitud.html',{'form':form,'solicitud':solicitud})

def eliminar_mi_solicitud(request, idsol):
    """ La funcion controla el boton de Cancelar en la lista Mis Reservas y Solicitudes, donde se listan las que pertenecen al
     usuario logueado actualmente"""
    solicitud= Solicitud.objects.get(solicitud_id=idsol)
    form= SolicitudConfirmForm(instance=solicitud)
    if request.method == 'POST':
        solicitud.estado = 'RCH'
        solicitud.save()
        return redirect('reserva_new:listar_reservas_user')
    return render(request,'reserva_new/eliminar_mi_solicitud.html',{'form':form,'solicitud':solicitud})


def notificar_rechazo(solicitud):
    """ La funcion auxiliar se encarga de enviar las notificaciones via email a los usuarios cuyas solicitudes han sido
    rechazadas"""
    fecha = solicitud.fecha_reserva.strftime('%Y-%m-%d')
    hora_i = solicitud.hora_inicio.strftime('%H:%M')
    hora_f = solicitud.hora_fin.strftime('%H:%M')
    email = solicitud.usuario.user.email
    send_mail(
        'Reserva Rechazada en Polimbae',
        'La solicitud de reserva para el dia: ' + fecha + ' y hora: ' + hora_i + '-' + hora_f + ' ha sido rechazada',
        'polimbae@gmail.com',
        [email],
        fail_silently=False,
    )

def notificar_confirmacion(solicitud):
    """ La funcion auxiliar se encarga de enviar las notificaciones via email a los usuarios cuyas solicitudes han sido
    confirmadas """

    fecha = solicitud.fecha_reserva.strftime('%Y-%m-%d')
    hora_i = solicitud.hora_inicio.strftime('%H:%M')
    hora_f = solicitud.hora_fin.strftime('%H:%M')
    email = solicitud.usuario.user.email
    send_mail(
        'Reserva Aceptada en Polimbae',
        'La solicitud de reserva para el dia: ' + fecha + ' y hora: ' + hora_i + '-' + hora_f + ' ha sido aprobada',
        'polimbae@gmail.com',
        [email],
        fail_silently=False,
    )
def solicitud_listar(request):
    """ La funcion maneja la vista de la lista de solicitudes a confirmar. La lista solo despliega las solicitudes
    que pertenencen a la fecha del dia siguiente, ya que la confirmacion se realiza un dia antes.
    La lista se ordena por categoria de usuario"""
    solicitud = Solicitud.objects.filter(estado='PEN')
    context = {'solicitud': solicitud}
    return render(request, 'reserva_new/lista_solicitud.html', context)
def notificar_cancelacion_reserva(reserva, motivo):
    fecha = reserva.fecha_reserva.strftime('%Y-%m-%d')
    hora_i = reserva.hora_inicio.strftime('%H:%M')
    hora_f = reserva.hora_fin.strftime('%H:%M')
    email = reserva.usuario.user.email
    send_mail(
        'Reserva Cancelada en Polimbae',
        'La Reserva para el dia: ' + fecha + ' y hora: ' + hora_i + '-' + hora_f + ' ha sido cancelada. '
                                                                                   'Motivo: '+motivo,
        'polimbae@gmail.com',
        [email],
        fail_silently=False,
    )

def entregar_recurso_reserva(request, idres):
    """ La funcion maneja el boton de Entrega de Recursos dentro de la lista de Reservas. Minutos antes de la hora de reserva,
    el administrador debe entregar el recurso al solicitante, momento en el cual marcara que el recurso ha sido entregado.
    1- La reserva pasara a estado de EN CURSO y el recurso a EN USO, solo si el recurso en cuestion se encontraba previamente en estado de Disponible,
    2- Si el recurso no se encuentra disponible a la hora de la reserva y el administrador intenta entregar el recurso, se desplegara un
    mensaje de que el recurso no esta disponible y que contacte con el usuario, presentandole los botones de volver al listado o cancelar la reserva actual
    """
    mensaje= None
    res= Reserva.objects.get(reserva_id=idres)
    hoy = date.today()
    now = datetime.now().time()


    reserva= Reserva.objects.filter(estado_reserva__in=['CONFIRMADA','EN CURSO'])


    if res.recurso_reservado.estado == 'DI':
            res.estado_reserva='EN CURSO'
            res.recurso_reservado.estado='EU'
            res.hora_inicio= now
            res.save()
            res.recurso_reservado.save()

            Log.objects.create(usuario=request.user,fecha_hora=datetime.now(),mensaje='Entrega Reserva '+res.__str__())

    else:
        mensaje= "El recurso no esta disponible"
        context = {'reserva': reserva, 'hoy': hoy, 'now': now, 'mensaje': mensaje}
        return render(request, 'reserva_new/lista_reserva.html', context)
    context = {'reserva': reserva, 'hoy': hoy, 'now': now, 'mensaje': mensaje}
    return render(request, 'reserva_new/lista_reserva.html',context)

def reserva_recurso_devuelto(request, idres):
    """ La funcion maneja el boton que marca la devolucion del recurso despues de finalizarse una reserva.
    1- La reserva pasa al estado de FINALIZADA y el recurso pasa al estado de DISPONIBLE
    2- Renderiza al listado de reservas """
    mensaje = None
    res = Reserva.objects.get(reserva_id=idres)
    hoy = date.today()
    now = datetime.now().time()
    reserva = Reserva.objects.filter(estado_reserva__in=['CONFIRMADA', 'EN CURSO'])

    res.estado_reserva = 'FINALIZADA'
    res.recurso_reservado.estado = 'DI'
    res.hora_fin = now
    res.save()
    res.recurso_reservado.save()

    Log.objects.create(usuario=request.user, fecha_hora=datetime.now(), mensaje='Devuelve Reserva ' + res.__str__())
    context = {'reserva': reserva, 'hoy': hoy, 'now': now, 'mensaje': mensaje}
    return render(request, 'reserva_new/lista_reserva.html', context)

def listar_reserva(request):
    """ Funcion que maneja la vista del listado de Reservas.
    1- La lista despliega las reservas que se confirman en la fecha de hoy al momento en que llega.
    2- Solo se listan las reservas cuyo estado es CONFIRMADA y EN CURSO"""
    hoy = date.today()
    now = datetime.now().time()
    if request.POST.get('mostrar_eliminados')== 'True':
        reserva= Reserva.objects.all()
        mostrar_eliminados= True
    else:
        reserva= Reserva.objects.filter(estado_reserva__in=['CONFIRMADA','EN CURSO'])
        mostrar_eliminados= False
    context = {'reserva': reserva, 'hoy':hoy, 'now':now, 'mostrar_eliminados': mostrar_eliminados}
    return render(request, 'reserva_new/lista_reserva.html', context)

def listar_reserva_user(request):
    """ Funcion que maneja la lista de Reservas y Solicitudes de los usuario logueados.
    1- El usuario tiene la opcion de Cancelar sus reservas y solicitudes en cualquier momento desde la lista
    2- Las solicitudes aparecen con estado de reserva PENDIENTE"""

    reserva = Reserva.objects.all()
    solicitud = Solicitud.objects.filter(estado='PEN')
    context = {'reserva': reserva, 'solicitud':solicitud}
    return render(request, 'reserva_new/lista_reserva_user.html', context)

def cancelar_reserva(request, idres):
    """ Funcion que maneja la Cancelacion de las Reservas.
    1- La reserva pasa al estado de CANCELADA
    2- Si el recurso no se encontraba disponible por estar asignado solo a esta Reserva, el mismo pasara a estar disponible para alguna reserva directa """
    hoy = date.today()
    now = datetime.now().time()
    reserva = Reserva.objects.get(reserva_id=idres)
    form = ReservaElimform(instance=reserva)
    if request.method == 'POST':
        motivo= request.POST['motivo']
        notificar_cancelacion_reserva(reserva,motivo)
        reserva.estado_reserva = 'CANCELADA'
        reserva.save()

        Log.objects.create(usuario=request.user, fecha_hora=datetime.now(), mensaje='Cancela Reserva ' + reserva.__str__())
        if reserva.recurso_reservado.estado == 'EU' and reserva.fecha_reserva == hoy and reserva.hora_inicio <= now and reserva.hora_fin > now:
            reserva.recurso_reservado.estado = 'DI'
            reserva.recurso_reservado.save()


        return redirect("reserva_new:reserva_listar")
    return render(request, 'reserva_new/eliminar_reserva.html',{'form':form, 'reserva':reserva})

def cancelar_mi_reserva(request, idres):
    """ El usuario puede cancelar su reserva desde la lista Mis Reservas y Solicitudes
    1- La reserva pasa al estado de CANCELADA
    2- Si el recurso esta en uso y la reserva corresponde al dia y hora actual, el recurso pasara a estar disponible"""
    reserva = Reserva.objects.get(reserva_id=idres)
    form = ReservaElimform(instance=reserva)
    hoy = date.today()
    now = datetime.now().time()
    if request.method == 'POST':
        reserva.estado_reserva = 'CANCELADA'
        reserva.save()

        Log.objects.create(usuario=request.user, fecha_hora=datetime.now(), mensaje='Cancela Reserva ' + reserva.__str__())
        if reserva.recurso_reservado.estado=='EU' and reserva.fecha_reserva== hoy and reserva.hora_inicio <= now and reserva.hora_fin > now:
            reserva.recurso_reservado.estado='DI'
            reserva.recurso_reservado.save()
        return redirect("reserva_new:listar_reservas_user")
    return render(request, 'reserva_new/eliminar_mi_reserva.html',{'form':form, 'reserva':reserva})


