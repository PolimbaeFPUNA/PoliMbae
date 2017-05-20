from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404,redirect, Http404
from django.utils.dateparse import parse_time, parse_datetime, parse_date
from app.reserva.forms import *
from app.reserva.models import ReservaGeneral, ListaReservaGeneral, ListaReservaEspecifica, ReservaEspecifica
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DateDetailView, View, DetailView
from app.recurso_pr.models import Recurso1, TipoRecurso1
from app.usuario.models import Profile
from PoliMbae import settings
from django.contrib.auth.models import User
from app.mantenimiento.models import Mantenimiento
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from datetime import date
from datetime import date, timedelta
import string


# Create your views here.

# vista basada en funciones

'''Funciones de Listados Reservas Generales '''


def reserva_general_listar(request):
    """ Funcion que Lista todos los registros creados del modelo de Reservas Generales
     y los envia al template listar_reserva.html"""
    qreserva = ReservaGeneral.objects.all().order_by('reserva_id')
    context = {'reserva': qreserva}
    return render(request, 'reserva/listar_reserva.html', context)


class ListarReservaGeneral(ListView):
    """ Funcion que Lista todos los registros creados del modelo de Reservas Generales
        y los envia al template listar_reserva.html"""
    model = ReservaGeneral
    template_name = 'reserva/listar_reserva.html'
    paginate_by = 7



'''Funciones de Listados de Lista de Reservas Generales Realizadas '''


def lista_reserva_general_listar(request):
    """ Lista auxiliar para verificar buen manejo de los registros de reservar para evitar
    coliciones con otras reservas.
    Los resultados son enviados a listar_reservas_realizadas"""
    qlista = ListaReservaGeneral.objects.all().order_by('lista_id')
    context = {'lista': qlista}
    return render(request, 'reserva/listar_reservas_realizadas.html', context)


class ListadoReservasAgendadas(ListView):
    """ Lista auxiliar para verificar buen manejo de los registros de reservar para evitar
      colisiones con otras reservas.
      Los resultados son enviados a listar_reservas_realizadas"""
    model = ListaReservaGeneral
    template_name = 'reserva/listar_reservas_realizadas.html'
    paginate_by = 7

'''Funcion Crear Reserva General '''


def crear_reserva(request, recurso_id):
    """ Se obtienen los datos ingresados en el formulario para realizar verificaciones de:
    1- Intento de reservas en horas inicio y fin iguales
    2- Fecha de reserva en horario indicado ya reservado por otro usuario
    3- El recurso no esta Disponible, ya que podria estar en matenimiento o solicitado
    4- Intento de reservar en fechas pasadas y no actuales o verideras
    5- Tipo de recurso en Mantenimiento por alguna falla o por mantenimiento preventivo
    6- El Tipo de recurso solicitado no es reservable.
    7- Formato de fechas incorrecto
    ListaReservaGeneral es la tabla auxiliar donde se organizan los datos para evitar colisiones."""
    mensaje = None
    if request.method == 'POST':
        form_reserva = ReservaGeneralForm(request.POST)
        usuario = request.POST.get('profile',)  # Guarda el ide del user, muestra la cedula en el template
        recurso = recurso_id  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva',)  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio',)  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin',)  # Hora fin introducida en el formulario
        reserva = ReservaGeneral.objects.all()  # No le encontre utilidad aun
        # Verificar User con CI
        #if verificar_cedula(usuario) == 1:
            #mensaje= "Error: Numero de Cedula Inexistente, verifique."
        # Verifica que la fecha no este agendada a la misma hora de inicio
        if verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: Ese recurso ya se encuentra reservado para la fecha y hora de inicio indicados"
        # Verifica que las horas inicio  y fin no sean iguales
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: La Hora de Inicio y Finalizacion son iguales. "
        # Verifica que las horas inicio  no sea mayor que la hora fin
        if verificar_hora(hora_inicio, hora_fin) == 2:
            mensaje = "Error: La Hora de Inicio es mayor que Hora de Finalizacion. "
        # Verifica que la hora de inicio no sea un intervalo del horario de otra reserva
        if verificar_horainicio_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: La Hora de Inicio es un intervalo del horario de otra reserva"
        # Verifica que la hora de fin no sea un intervalo del horario de otra reserva
        if verificar_horafin_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: La Hora de Finalizacion es un intervalo del horario de otra reserva"
        # Verifica el estado del recurso esta Disponible para ser reservado.
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        # Verifica que el recurso sea reservable
        if verificar_reservable(recurso) == 1:
            mensaje = "Error: El recurso NO es Reservable "
        # Verifica que la fecha introducida no sea desfasada
        if fecha_vieja(fecha_reserva) == 1:
            mensaje = "Error: Fecha de Reserva desfasada. Debe ser actual o para reservas futuras. "
        # Verifica que la fecha tenga el formato correcto
        if fecha_vieja(fecha_reserva) == 2:
            mensaje = "Error: Formato de fechas incorrecto, utilize 'Y-m-d' "
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Preventivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 1:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Preventivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Correctivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 2:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Correctivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento en etapas de finalizacion
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 3:
            mensaje = "Error: El recurso se encuentra en etapa de finalizacion del Mantenimiento"
        if verificar_recurso_especifico(recurso, fecha_reserva) == 1:
            mensaje = "Error: El recurso es Solicitado en Reserva Especifica, no se encuentra disponible"
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores

            u = Profile.objects.get(user__username=usuario)
            ListaReservaGeneral.objects.create(recurso_reservado=recurso, usuario=u.cedula, estado_reserva='RE',
                                               fecha_reserva=request.POST['fecha_reserva'],
                                               hora_inicio=request.POST['hora_inicio'],
                                               hora_fin=request.POST['hora_fin'])
            person = None
            user = Profile.objects.all()

            for u in user:
                if u.user.username == usuario:
                    person = u.id
            ReservaGeneral.objects.create(profile_id=person, recurso_id=recurso, fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])
            return redirect('reserva:reserva_listar')
    else:
        form_reserva = ReservaGeneralForm()
    context = {
        'form': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/crear_reserva.html', context)


def verificar_recurso_especifico(recurso, fecha_reserva):
    nro = int(recurso)
    dia = parse_date(fecha_reserva)
    especifica = ListaReservaEspecifica.objects.all()
    for r in especifica:
        if r.recurso_reservado == nro:
            if r.fecha_reserva == dia:
                return 1
    return 0


'''Verificacion de usuario con CI iguales al user '''

def verificar_cedula(usuario):
    user = Profile.objects.all()
    for u in user:
        if u.cedula == usuario:
            return 0
    return 1

'''Verificacion de reserva del recurso en Fechas y Horarios de Mantenimientos'''


def recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin):
    """ En esta funcion se controlan los fechas de mantenimientos en colision con fecha de reserva
    Retorna 1 si es Matenimiento Preverntivo en fecha y hora de inicio
    Retorna 2 si es Mantenimiento Correctivo en fecha y hora de inicio
    Retorna 3 si el tipo de recurso todavia se encuentra en etapa de finalizacion"""
    mantenimiento = Mantenimiento.objects.all()
    nro = int(recurso)
    dia = parse_date(fecha_reserva)
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    for recu in mantenimiento:
        if recu.fecha_entrega == dia and recu.recurso_id == nro:
            if recu.tipo == 'Preventivo':
                return 1
            if recu.tipo == 'Correctivo':
                return 2
        if recu.fecha_fin == dia and recu.recurso_id == nro:
            return 3
    return 0

''' Funcion para controlar que la hora de inicio dada no sea igual a una existete o
    este estre la hora de inicio y fin de alguna reserva realizada'''


def verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso):
    """Funcion que controla que  el recurso no este reservado para la fecha y hora de inicio existentes
    retorna 1 si se encuentra la colision"""
    agenda = ListaReservaGeneral.objects.all()  # Retorana todos los objetos de la tabla
    h1 = parse_time(hora_inicio)  # cambio de text a hora
    h2 = parse_time(hora_fin)
    dia = parse_date(fecha_reserva)
    nro = int(recurso)
    dia = parse_date(fecha_reserva)
    for p in agenda:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        if p.recurso_reservado == nro:
            if p.fecha_reserva == dia:
                if hora1 == h1:
                    return 1
    return 0


def verificar_horainicio_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso):
    """ Funcion que controla que en la fecha de reserva indicaca, no se tenga la
    hora de inicio de reserva en forma intermedia en otro horario ya reservado"""
    agenda = ListaReservaGeneral.objects.all()  # Retorana todos los objetos de la tabla
    h1 = parse_time(hora_inicio)  # cambio de text a hora
    h2 = parse_time(hora_fin)
    dia = parse_date(fecha_reserva)
    nro = int(recurso)
    dia = parse_date(fecha_reserva)
    for p in agenda:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        if p.recurso_reservado == nro:
            if p.fecha_reserva == dia:
                if h1 > hora1:
                    if h1 < hora2:
                        return 1
    return 0


def verificar_horafin_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso):
    """ Funcion que controla que en la fecha de reserva indicaca, no se tenga la
       hora de finalizacion de reserva en forma intermedia en otro horario ya reservado"""
    agenda = ListaReservaGeneral.objects.all()  # Retorana todos los objetos de la tabla
    h1 = parse_time(hora_inicio)  # cambio de text a hora
    h2 = parse_time(hora_fin)
    dia = parse_date(fecha_reserva)
    nro = int(recurso)
    dia = parse_date(fecha_reserva)
    for p in agenda:  # Busca en cada tupla
        hora1 = p.hora_inicio
        hora2 = p.hora_fin
        if p.recurso_reservado == nro:
            if p.fecha_reserva == dia:
                if h2 > hora2:
                    if h2 < hora2:
                        return 1
    return 0


'''Esta funcion controla que la hora de inicio no sea mayor que la hora final'''


def verificar_hora(hora_inicio, hora_fin):
    """ Funcion que controla el error de hora de inicio mayor que la hora de finalizacion"""
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    if h2 == h1:
        return 1
    if h2 < h1:
        return 2
    return 0


def verificar_dia(fecha_reserva):
    agenda = ListaReservaGeneral.objects.all()
    dia = parse_date(fecha_reserva)
    for p in agenda:
        if p.fecha_reserva == dia:
            return 1
    return 0


'''Se verifica que el estado del recurso sea Disponible para poder reservarlo'''


def verificar_estado(recurso):
    recu = Recurso1.objects.all()
    nro = int(recurso)
    for p in recu:
        if p.estado == 'RE' and p.recurso_id == nro:
            return 1
        if p.estado == 'FU' and p.recurso_id == nro:
            return 1
        if p.estado == 'EU' and p.recurso_id == nro:
            return 1
        if p.estado == 'EM' and p.recurso_id == nro:
            return 1
        if p.estado == 'SO' and p.recurso_id == nro:
            return 1
    return 0

'''Se verifica que el recurso sea reservable'''


def verificar_reservable(recurso):
    recu = Recurso1.objects.all()
    nro = int(recurso)
    for p in recu:
        if p.recurso_id == nro:
            if p.tipo_id.reservable == False:
                return 1
    return 0


'''Se verifica que el recurso no este en Mantenimiento Preventivo en fecha de reserva introducida por el usuario'''


def verificar_mantenimiento(recurso, fecha_reserva):
    recu = Recurso1.objects.all()
    dia = parse_date(fecha_reserva)
    nro = int(recurso)
    for p in recu:
        if p.recurso_id == nro:
            fe = p.tipo_id.fecha_mantenimiento
            fe3 = fe.date()
            if fe3 == dia:
                return 1
    return 0

'''Se verifica que el recurso sea reservable'''


def fecha_vieja(fecha_reserva):
    dia = parse_date(fecha_reserva)
    if dia is None:
        return 2
    if dia < date.today():
        return 1
    return 0



'''Busqueda de un recurso para su Reserva.
    La busqueda se realiza por nombre del tipo de recurso indicado por el usuario.
    Se envian los resultados de la busqueda a la misma vista, el template suministra
    una tabla de recursos existentes y que coinciden con el dato de busqueda'''


def buscar(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            recursos = Recurso1.objects.filter(tipo_id__nombre_recurso__icontains=q)
            return render(request, 'reserva/detalle.html', {'recursos': recursos, 'query': q})
    return render(request, 'reserva/detalle.html', {'error': error})


''' Cuando el usuario cancela la reserva, se elimina el registro, tanto en las Reservas Generales
    como en la lista auxiliar '''


def borrar_reserva(request, reserva_id):
    reserva = ReservaGeneral.objects.get(reserva_id=reserva_id)
    lista_reserva = ListaReservaGeneral.objects.all()
    if request.method == 'POST':
        reserva.delete()
        for p in lista_reserva:
            if p.recurso_reservado == reserva.recurso_id and p.fecha_reserva == reserva.fecha_reserva:
                if p.hora_inicio == reserva.hora_inicio and p.hora_fin == reserva.hora_fin:
                    p.delete()
        return redirect('reserva:reserva_listar')
    return render(request, 'reserva/reserva_eliminar.html', {'reserva': reserva})


''' Recibe el id de la reserva y lo modifica atendiendo que:
    1- La fecha de reserva coincida con otra en los mismos horarios
    2- Que los horarios sean introducidos coherentemente
    3- El estado del Recurso de estar Disponible
    Para ubicarlo nuevamente en la lista auxiliar (ListaReservaGeneral) se procede a eliminar
    el registro y volver a crearlo, evitandose asi duplicidades
    4- No este en mantenimiento Preventivo o Correctivo
    5- Fecha nueva de reserva Desfasada
    6- Nuevos horarios en colision con otros existentes'''


def reserva_modificar(request, reserva_id):
    """ Recibe el id de la reserva y lo modifica atendiendo que:
        1- La fecha de reserva coincida con otra en los mismos horarios
        2- Que los horarios sean introducidos coherentemente
        3- El estado del Recurso de estar Disponible
        Para ubicarlo nuevamente en la lista auxiliar (ListaReservaGeneral) se procede a eliminar
        el registro y volver a crearlo, evitandose asi duplicidades
        4- No este en mantenimiento Preventivo o Correctivo
        5- Fecha nueva de reserva Desfasada
        6- Nuevos horarios en colision con otros existentes"""
    mensaje = None
    nro = int(reserva_id)
    reserva = ReservaGeneral.objects.get(reserva_id=reserva_id)
    lista_reserva = ListaReservaGeneral.objects.all()
    if request.method == 'GET':
        form_reserva = ReservaGeneralForm2(instance=reserva)
    else:
        for p in lista_reserva:
            if p.recurso_reservado == reserva.recurso_id and p.fecha_reserva == reserva.fecha_reserva:
                if p.hora_inicio == reserva.hora_inicio and p.hora_fin == reserva.hora_fin:
                    p.delete()
        form_reserva = ReservaGeneralForm2(request.POST, instance=reserva)
        recurso = request.POST.get('recurso',)  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva', )  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio', )  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin', )  # Hora fin introducida en el formulario

        if verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: Ese recurso ya se encuentra reservado para la fecha y hora de inicio indicados"
        # Verifica que las horas inicio  y fin no sean iguales
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: La Hora de Inicio y Finalizacion son iguales. "
        # Verifica que las horas inicio  no sea mayor que la hora fin
        if verificar_hora(hora_inicio, hora_fin) == 2:
            mensaje = "Error: La Hora de Inicio mayor que hora de Finalizacion. "
        # Verifica que la hora de inicio no sea un intervalo del horario de otra reserva
        if verificar_horainicio_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: La Hora de Inicio es un intervalo del horario de otra reserva"
        # Verifica que la hora de fin no sea un intervalo del horario de otra reserva
        if verificar_horafin_intermedia(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: La Hora de Finalizacion es un intervalo del horario de otra reserva"
        # Verifica el estado del recurso esta Disponible para ser reservado.
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        # Verifica que el recurso sea reservable
        if verificar_reservable(recurso) == 1:
            mensaje = "Error: El recurso NO es Reservable "
        # Verifica que la fecha introducida no sea desfasada
        if fecha_vieja(fecha_reserva) == 1:
            mensaje = "Error: Fecha de Reserva desfasada. Debe ser actual o para reservas futuras. "
        # Verifica que la fecha tenga el formato correcto
        if fecha_vieja(fecha_reserva) == 2:
            mensaje = "Error: Formato de fechas incorrecto, utilize 'Y-m-d' "
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Preventivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 1:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Preventivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Correctivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 2:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Correctivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento en etapas de finalizacion
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 3:
            mensaje = "Error: El recurso se encuentra en etapa de finalizacion del Mantenimiento"
        if verificar_recurso_especifico(recurso, fecha_reserva) == 1:
            mensaje = "Error: El recurso es Solicitado en Reserva Especifica, no se encuentra disponible"
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores
            ListaReservaGeneral.objects.create(recurso_reservado=recurso, estado_reserva='RE',
                                               fecha_reserva=request.POST['fecha_reserva'],
                                               hora_inicio=request.POST['hora_inicio'],
                                               hora_fin=request.POST['hora_fin'])
            if form_reserva.is_valid():
                form_reserva.save()
            return redirect('reserva:reserva_listar')
    context = {
        'form_reserva': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/modificar_reserva.html', context)


'''Funciones para listar Reservas Especificas Realizadas '''


def reserva_especifica_listar(request):
    """ Funcion que Lista todos los registros creados del modelo de Reservas Especificas
     y los envia al template listar_reserva_especifica.html"""
    qespecifica = ReservaEspecifica.objects.all().order_by('reserva_id')
    context = {'reservaes': qespecifica}
    return render(request, 'reserva/listar_reserva_especifica.html', context)


class ListarReservaEspecifica(ListView):
    model = ReservaEspecifica
    template_name = 'reserva/listar_reserva_especifica.html'
    paginate_by = 10


'''Funciones de Agenda de Lista de Reservas Especificas Realizadas '''


def lista_reserva_especifica_listar(request):
    qlista = ListaReservaEspecificaForm.objects.all().order_by('lista_id')
    context = {'lista': qlista}
    return render(request, 'reserva/listar_especifica_realizadas.html', context)



class ListadoReservasEspecificasAgendadas(ListView):
    model = ListaReservaEspecifica
    template_name = 'reserva/listar_especifica_realizadas.html'
    paginate_by = 10


def buscar_especifica(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            recursos = Recurso1.objects.filter(tipo_id__nombre_recurso__icontains=q)
            return render(request, 'reserva/detalle_especifica.html', {'recursos': recursos, 'query': q})
    return render(request, 'reserva/detalle_especifica.html', {'error': error})


def listar_reservas_hoy(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            usuario = ListaReservaEspecifica.objects.filter(usuario=q)
            return render(request, 'reserva/lista_hoy.html', {'usuario': usuario, 'query': q})
    return render(request, 'reserva/lista_hoy.html', {'error': error})


def listar_reservas_hoy2(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            usuario = ListaReservaGeneral.objects.filter(usuario=q)
            return render(request, 'reserva/lista_hoy2.html', {'usuario': usuario, 'query': q})
    return render(request, 'reserva/lista_hoy2.html', {'error': error})


def confirmar_reserva_especifica(request, lista_id):
    reserva = ListaReservaEspecifica.objects.get(lista_id=lista_id)
    if request.method == 'GET':
        form = ListaReservaEspecificaForm2(instance=reserva)
    else:
        form = ListaReservaEspecificaForm2(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
        return redirect('reserva:agenda_especifica_listar')
    return render(request, 'reserva/confirmar_reserva.html', {'form': form})


def confirmar_reserva_general(request, lista_id):
    reserva = ListaReservaGeneral.objects.get(lista_id=lista_id)
    if request.method == 'GET':
        form = ListaReservaGeneralForm2(instance=reserva)
    else:
        form = ListaReservaGeneralForm2(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
        return redirect('reserva:agenda_listar')
    return render(request, 'reserva/confirmar_reserva.html', {'form': form})


def ver_prioridad(usuario):
    reserva = ReservaEspecifica.objects.all()
    for p in reserva:
        if p.profile.cedula == usuario:
            cate = p.profile.categoria
            if cate == 'Institucional':
                prioridad = 8
                return prioridad
            if cate == 'Titular':
                prioridad = 7
                return prioridad
            if cate == 'Adjunto':
                prioridad = 6
                return prioridad
            if cate == 'Asistente':
                prioridad = 5
                return prioridad
            if cate == 'Encargado de Catedra':
                prioridad = 4
                return prioridad
            if cate == 'Auxiliar de Ensenanza':
                prioridad = 3
                return prioridad
            if cate == 'Alumno':
                prioridad = 2
                return prioridad
            if cate == 'Funcionario':
                prioridad = 1
                return prioridad
    return 0
'''Funcion Crear Reserva Especifica '''


def crear_reserva_especifica(request, recurso_id):
    mensaje = None
    if request.method == 'POST':
        form_reserva = ReservaEspecificaForm(request.POST)
        usuario = request.POST.get('profile',)  # Guarda el ide del user, muestra la cedula en el template
        recurso = recurso_id  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva',)  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio',)  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin',)  # Hora fin introducida en el formulario

        if verificar_cedula(usuario) == 1:
            mensaje= "Error: Numero de Cedula Inexistente, verifique."
        # Verifica que las horas inicio  y fin no sean iguales
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: La Hora de Inicio y Finalizacion son iguales. "
        # Verifica que las horas inicio  no sea mayor que la hora fin
        if verificar_hora(hora_inicio, hora_fin) == 2:
            mensaje = "Error: La Hora de Inicio es mayor que Hora de Finalizacion. "
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        if verificar_reservable(recurso) == 1:
            mensaje = "Error: El recurso NO es Reservable "
        # Verifica que la fecha introducida no sea desfasada
        if fecha_vieja(fecha_reserva) == 1:
            mensaje = "Error: Fecha de Reserva desfasada. Debe ser actual o para reservas futuras. "
        # Verifica que la fecha tenga el formato correcto
        if fecha_vieja(fecha_reserva) == 2:
            mensaje = "Error: Formato de fechas incorrecto, utilize 'Y-m-d' "
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Preventivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 1:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Preventivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Correctivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 2:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Correctivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento en etapas de finalizacion
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 3:
            mensaje = "Error: El recurso se encuentra en etapa de finalizacion del Mantenimiento"
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores

            person = None
            cedula = None
            user = Profile.objects.all()
            for u in user:
                if u.cedula == usuario:
                    person = u.id
                    cedula = u.cedula

            ReservaEspecifica.objects.create(profile_id=person, recurso_id=recurso,
                                             fecha_reserva=request.POST['fecha_reserva'],
                                             hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])
            prioridad = ver_prioridad(usuario)
            ListaReservaEspecifica.objects.create(recurso_reservado=recurso, usuario=cedula, estado_reserva='SO', prioridad=prioridad,
                                                  fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])

            return redirect('reserva:reserva_especifica_listar')
    else:
        form_reserva = ReservaGeneralForm()
    context = {
        'form': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/crear_reserva_especifica.html', context)


def borrar_reserva_especifica(request, reserva_id):
    reserva = ReservaEspecifica.objects.get(reserva_id=reserva_id)
    lista_reserva_especifica = ListaReservaEspecifica.objects.all()
    if request.method == 'POST':
        reserva.delete()
        for p in lista_reserva_especifica:
            if p.recurso_reservado == reserva.recurso_id and p.fecha_reserva == reserva.fecha_reserva:
                if p.hora_inicio == reserva.hora_inicio and p.hora_fin == reserva.hora_fin:
                    p.delete()
        return redirect('reserva:reserva_especifica_listar')
    return render(request, 'reserva/reserva_especifica_eliminar.html', {'reserva': reserva})



def modificar_reserva_especifica(request, reserva_id):
    mensaje = None
    nro = int(reserva_id)
    cedula = None
    reserva2 = ReservaEspecifica.objects.all()
    reserva = ReservaEspecifica.objects.get(reserva_id=reserva_id)
    lista_reserva_especifica = ListaReservaEspecifica.objects.all()
    for u in reserva2:
        if u.reserva_id == nro:
            cedula = u.profile.cedula
    if request.method == 'GET':
        form_reserva = ReservaEspecificaForm2(instance=reserva)
    else:
        for p in lista_reserva_especifica:
            if p.recurso_reservado == reserva.recurso.recurso_id and p.fecha_reserva == reserva.fecha_reserva:
                if p.hora_inicio == reserva.hora_inicio and p.hora_fin == reserva.hora_fin:
                    p.delete()
        form_reserva = ReservaEspecificaForm2(request.POST, instance=reserva)
        recurso = request.POST.get('recurso',)  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva', )  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio', )  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin', )  # Hora fin introducida en el formulario
        # Verifica que las horas inicio  y fin no sean iguales
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: La Hora de Inicio y Finalizacion son iguales. "
        # Verifica que las horas inicio  no sea mayor que la hora fin
        if verificar_hora(hora_inicio, hora_fin) == 2:
            mensaje = "Error: La Hora de Inicio es mayor que Hora de Finalizacion. "
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        if verificar_reservable(recurso) == 1:
            mensaje = "Error: El recurso NO es Reservable "
        # Verifica que la fecha introducida no sea desfasada
        if fecha_vieja(fecha_reserva) == 1:
            mensaje = "Error: Fecha de Reserva desfasada. Debe ser actual o para reservas futuras. "
        # Verifica que la fecha tenga el formato correcto
        if fecha_vieja(fecha_reserva) == 2:
            mensaje = "Error: Formato de fechas incorrecto, utilize 'Y-m-d' "
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Preventivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 1:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Preventivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento Correctivo
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 2:
            mensaje = "Error: El recurso se encuentra en Mantenimiento Correctivo en fecha y hora de inicio indicados"
        # Verifica la fecha y horario de reserva no este en colision con el Mantenimiento en etapas de finalizacion
        if recurso_mantenimiento(recurso, fecha_reserva, hora_inicio, hora_fin) == 3:
            mensaje = "Error: El recurso se encuentra en etapa de finalizacion del Mantenimiento"
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores

            prioridad = ver_prioridad(cedula)
            ListaReservaEspecifica.objects.create(recurso_reservado=recurso, usuario=cedula, estado_reserva='SO', prioridad=prioridad,
                                                fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])
            if form_reserva.is_valid():
                form_reserva.save()
            return redirect('reserva:reserva_especifica_listar')
    context = {
        'form_reserva': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/modificar_especifica.html', context)
