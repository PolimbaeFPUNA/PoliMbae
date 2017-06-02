from django.shortcuts import render, redirect
from app.reserva_new.models import Solicitud, Reserva
from app.recurso_pr.models import Recurso1, TipoRecurso1
from app.reserva_new.forms import *
from app.usuario.models import Profile
from django.utils.dateparse import parse_date, parse_time
from django.views.generic import ListView
from django.core.mail import send_mail
# Create your views here.

def crear_solicitud(request):
    form= SolicitudForm()
    mensaje= None
    recurso_id=None
    if request.method == 'POST':

        if request.POST.get('guardar'):
            usuario= Profile.objects.get(user__username=request.POST['profile'])
            fecha= request.POST['fecha_reserva']
            hora_inicio= request.POST['hora_inicio']
            hora_fin= request.POST['hora_fin']
            tipo= TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])
            recurso= buscar_recurso_disponible(fecha, hora_inicio, hora_fin, tipo)
            Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                        usuario=usuario, recurso=recurso)
    return render(request, "reserva_new/crear_solicitud.html", {'form':form})

def crear_solicitud_especifica(request):
    form= SolicitudForm()
    mensaje= None
    recurso_id=None
    if request.method == 'POST':

        if request.POST.get('guardar'):
            fecha= request.POST['fecha_reserva']
            hora_inicio= request.POST['hora_inicio']
            hora_fin= request.POST['hora_fin']
            tipo= TipoRecurso1.objects.get(tipo_id=request.POST['tipo_recurso'])
            recurso= buscar_recurso_disponible(fecha, hora_inicio, hora_fin, tipo)
            Solicitud.objects.create(fecha_reserva=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
                                        usuario=request.user, recurso=recurso)

    return render(request, "reserva_new/crear_solicitud.html", {'form':form})

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
    mensaje=None
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

    lista_solicitud= Solicitud.objects.filter(recurso=solicitud.recurso)

    for s in lista_solicitud:
        if s.fecha_reserva == f and s.solicitud_id != solicitud.solicitud_id:
            if s.hora_inicio >= h1 and s.hora_inicio < h2:
                notificar_rechazo(s)
                s.delete()
            if s.hora_fin > h1 and s.hora_fin < h2:
                notificar_rechazo(s)
                s.delete()
            if s.hora_inicio <= h1 and s.hora_fin >= h2:
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

def reserva_especifica_listar(request):

    solicitud = Solicitud.objects.all()
    #aca ordenar por prioridad
    context = {'solicitud': solicitud}
    return render(request, 'reserva_new/lista_solicitud.html', context)

class ListarSolicitud(ListView):
    model = Solicitud
    template_name = 'reserva_new/lista_solicitud.html'
    paginate_by = 10