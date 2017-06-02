from django.shortcuts import render, redirect
from app.reserva_new.models import Solicitud, Reserva
from app.recurso_pr.models import Recurso1, TipoRecurso1
from app.reserva_new.forms import *
from app.usuario.models import Profile
from django.utils.dateparse import parse_date, parse_time
from django.views.generic import ListView
from django.core.mail import send_mail
from datetime import datetime,timedelta, date
# Create your views here.

def crear_solicitud(request):
    if request.method == 'POST':
        form= SolicitudForm(initial={'tipo_recurso':request.POST.get('tipo_recurso'), 'fecha_reserva':request.POST.get('fecha_reserva'),'hora_inicio': request.POST.get('hora_inicio'),'hora_fin':request.POST.get('hora_fin')})
    else:
        form = SolicitudForm()
    form.fields['tipo_recurso'].widget.attrs['onChange'] = 'document.getElementById("get_datos").click();'
    if request.POST.get('tipo_recurso') != '':
        form.fields['recurso'].queryset = Recurso1.objects.filter(tipo_id=request.POST.get('tipo_recurso'))
    else:
        form.fields['recurso'].queryset = Recurso1.objects.none()
    mensaje= None
    recurso_id=None
    if request.method == 'POST' and request.POST.get('guardar'):

            usuario= Profile.objects.get(user__username=request.POST['profile'])
            fecha= request.POST['fecha_reserva']
            hora_inicio= request.POST['hora_inicio']
            hora_fin= request.POST['hora_fin']
            tipo= TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])
            hoy= date.today()
            f= parse_date(fecha)
            if request.POST['recurso'] == '' and f != hoy:
                recurso= buscar_recurso_disponible(fecha, hora_inicio, hora_fin, tipo)
                Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                        usuario=usuario, recurso=recurso)

                return redirect("reserva_new:listar_reservas_user")
            elif f == hoy and request.POST['recurso'] == '':
                recurso= verificar_reserva(fecha, hora_inicio, hora_fin, tipo)

                if recurso:
                    Reserva.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                             usuario=usuario, recurso_reservado=recurso,estado_reserva='CONFIRMADA')
                    return redirect("reserva_new:listar_reservas_user")

                else:
                    mensaje= "No hay recursos disponibles para fecha y rango de horas solicitada"
            elif f == hoy and request.POST['recurso'] != '':
                recurso= Recurso1.objects.get(recurso_id=request.POST['recurso'])
                if verificar_reserva_recurso(fecha, hora_inicio, hora_fin, tipo,recurso):
                    Reserva.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                             usuario=usuario, recurso_reservado=recurso, estado_reserva='CONFIRMADA')
                    return redirect("reserva_new:listar_reservas_user")
                else:
                    mensaje = "El recurso no esta disponible en fecha y rango de horas solicitada"

            else:
                recurso= Recurso1.objects.get(recurso_id=request.POST['recurso'])
                Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                         usuario=usuario, recurso=recurso)
                return redirect("reserva_new:listar_reservas_user")

    return render(request, "reserva_new/crear_solicitud.html", {'form':form, 'mensaje': mensaje})
def verificar_reserva_recurso(fecha, hora_inicio, hora_fin, tipo,recurso):
    r = None
    f = parse_date(fecha)
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    lista_reserva = Reserva.objects.all()

    for r in lista_reserva:
        if recurso.recurso_id == r.recurso_reservado.recurso_id:
            if r.fecha_reserva == f:

                if r.hora_inicio >= h1 and r.hora_inicio < h2:
                   return False

                elif r.hora_fin > h1 and r.hora_fin < h2:
                    return False

                elif r.hora_inicio <= h1 and r.hora_fin >= h2:
                    return False

    return True
def verificar_reserva(fecha, hora_inicio, hora_fin, tipo):

    f = parse_date(fecha)
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    h2_aux = (datetime.combine(date.today(), h2) + timedelta(minutes=15)).time()
    h1_aux = (datetime.combine(date.today(), h1) - timedelta(minutes=15)).time()
    lista_reserva= Reserva.objects.all()
    lista_recurso = Recurso1.objects.filter(tipo_id=tipo.tipo_id)
    for recurso in lista_recurso:
        count=0
        flag=None
        for r in lista_reserva:
            if recurso.recurso_id == r.recurso_reservado.recurso_id:
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
    r=None
    f= parse_date(fecha)
    h1= parse_time(hora_inicio)
    h2= parse_time(hora_fin)
    count= 0
    previo=99999
    lista_solicitud= Solicitud.objects.filter(recurso__tipo_id= tipo.tipo_id)
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
    solicitud= Solicitud.objects.get(solicitud_id=idsol)

    form= SolicitudConfirmForm(instance=solicitud)

    if request.method == 'POST':

            Reserva.objects.create(usuario=solicitud.usuario, recurso_reservado=solicitud.recurso, fecha_reserva=solicitud.fecha_reserva,
                                    hora_inicio=solicitud.hora_inicio, hora_fin=solicitud.hora_fin, estado_reserva='CONFIRMADA')
            rechazar_colisionadas(solicitud)
            solicitud.delete()
            return redirect("reserva_new:solicitud_listar")

    return render(request, "reserva_new/confirmar_solicitud.html",{'form':form, 'solicitud':solicitud})

def rechazar_colisionadas(solicitud):
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
                s.delete()
            elif s.hora_fin > h1 and s.hora_fin < h2:
                notificar_rechazo(s)
                s.delete()
            elif s.hora_inicio  <= h1 and s.hora_fin >= h2:
                notificar_rechazo(s)
                s.delete()
            elif h2_aux > s.hora_inicio and h1 < s.hora_inicio:
                notificar_rechazo(s)
                s.delete()
            elif h1_aux < s.hora_fin and s.hora_inicio < h1:
                notificar_rechazo(s)
                s.delete()


def notificar_rechazo(solicitud):
    fecha = solicitud.fecha_reserva.strftime('%Y-%m-%d')
    hora_i = solicitud.hora_inicio.strftime('%H:%M')
    hora_f = solicitud.hora_fin.strftime('%H:%M')
    email = solicitud.usuario.user.email
    send_mail(
        'Solicitud de Reserva Rechazada en Polimbae',
        'La solicitud de reserva para el dia: ' + fecha + ' y hora: ' + hora_i + '-' + hora_f + ' ha sido rechazada',
        'polimbae@gmail.com',
        [email],
        fail_silently=False,
    )

def solicitud_listar(request):

    solicitud = Solicitud.objects.all().order_by('usuario__categoria')
    context = {'solicitud': solicitud}
    return render(request, 'reserva_new/lista_solicitud.html', context)

def entregar_recurso_reserva(request, idres):
    reserva= Reserva.objects.get(reserva_id=idres)
    form = Reservaform(instance=reserva)
    if request.method == 'POST':
        if reserva.recurso_reservado.estado == 'DI':
            reserva.estado_reserva='EN CURSO'
            reserva.recurso_reservado.estado='EU'
            reserva.save()
            reserva.recurso_reservado.save()
            return redirect("reserva_new:reserva_listar")
        else:
            #buscar algun recurso disponible para reasignar a la reserva, manualmente
             return redirect("reserva_new:buscar_disponible")
    return render(request, 'reserva_new/entrega_recurso.html',{'form':form, 'reserva':reserva})

def listar_reserva(request):

    reserva= Reserva.objects.all()
    context = {'reserva': reserva}
    return render(request, 'reserva_new/lista_reserva.html', context)

def listar_reserva_user(request):
    reserva = Reserva.objects.all()
    solicitud = Solicitud.objects.all()
    usuario= request.user.id
    context = {'reserva': reserva, 'user': usuario, 'solicitud':solicitud}
    return render(request, 'reserva_new/lista_reserva_user.html', context)



