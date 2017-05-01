from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.utils.dateparse import parse_time, parse_datetime, parse_date
from app.reserva.forms import ReservaGeneralForm, ListaReservaGeneralForm, ListaReservaEspecificaForm, ReservaEspecificaForm
from app.reserva.models import ReservaGeneral, ListaReservaGeneral, ListaReservaEspecifica, ReservaEspecifica
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DateDetailView, View, DetailView
from app.recurso.models import Recurso1, TipoRecurso1
from django.http import JsonResponse
from django.db.models import Q
from django.template import RequestContext
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
    model = ReservaGeneral
    template_name = 'reserva/listar_reserva.html'
    paginate_by = 10


'''Funciones de Listados de Lista de Reservas Generales Realizadas '''


def lista_reserva_general_listar(request):
    qlista = ListaReservaGeneral.objects.all().order_by('lista_id')
    context = {'lista': qlista}
    return render(request, 'reserva/listar_reservas_realizadas.html', context)


class ListadoReservasAgendadas(ListView):
    model = ListaReservaGeneral
    template_name = 'reserva/listar_reservas_realizadas.html'
    paginate_by = 10

'''Funcion Crear Reserva General '''


def crear_reserva(request, recurso_id):
    mensaje = None
    if request.method == 'POST':
        form_reserva = ReservaGeneralForm(request.POST)
        usuario = request.POST.get('profile',)  # Guarda el ide del user, muestra la cedula en el template
        recurso = recurso_id  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva',)  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio',)  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin',)  # Hora fin introducida en el formulario
        reserva = ReservaGeneral.objects.all()  # No le encontre utilidad aun

        # Verifica que la fecha no este agendada a la misma hora de inicio
        if verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: Ese recurso ya se encuentra reservado para la fecha y hora de inicio indicados"
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: Horas Incorrectas "
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores
            ListaReservaGeneral.objects.create(recurso_reservado=recurso, estado_reserva='RE',
                                               fecha_reserva=request.POST['fecha_reserva'],
                                               hora_inicio=request.POST['hora_inicio'],
                                               hora_fin=request.POST['hora_fin'])

            ReservaGeneral.objects.create(profile_id=request.POST['profile'], recurso_id=recurso, fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])
            return redirect('reserva:reserva_listar')
    else:
        form_reserva = ReservaGeneralForm()
    context = {
        'form': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/crear_reserva.html', context)


''' Funcion para controlar que la hora de inicio dada no sea igual a una existete o
    este estre la hora de inicio y fin de alguna reserva realizada'''


def verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso):
    agenda = ListaReservaGeneral.objects.all()  # Retorana todos los objetos de la tabla
    h1 = parse_time(hora_inicio)  # cambio de text a hora
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
                if h1 > hora1:
                    if h1 < hora2:
                        return 1
    return 0


'''Esta funcion controla que la hora de inicio no sea mayor que la hora final'''


def verificar_hora(hora_inicio, hora_fin):
    h1 = parse_time(hora_inicio)
    h2 = parse_time(hora_fin)
    if h2 <= h1:
        return 1
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
    Para ubicarlo denuevo en la lista auxiliar (ListaReservaGeneral) se procede a eliminar
    el registro y volver a crearlo, evitandose asi duplicidades'''


def reserva_modificar(request, reserva_id):
    mensaje = None
    reserva = ReservaGeneral.objects.get(reserva_id=reserva_id)
    lista_reserva = ListaReservaGeneral.objects.all()
    if request.method == 'GET':
        form = ReservaGeneralForm(instance=reserva)
    else:
        for p in lista_reserva:
            if p.recurso_reservado == reserva.recurso_id and p.fecha_reserva == reserva.fecha_reserva:
                if p.hora_inicio == reserva.hora_inicio and p.hora_fin == reserva.hora_fin:
                    p.delete()
        form = ReservaGeneralForm(request.POST, instance=reserva)
        usuario = request.POST.get('profile', )  # Guarda el ide del user, muestra la cedula en el template
        recurso = reserva.recurso.recurso_id  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva', )  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio', )  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin', )  # Hora fin introducida en el formulario
        reserva = ReservaGeneral.objects.all()  # No le encontre utilidad aun

        # Verifica que la fecha no este agendada a la misma hora de inicio
        if verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: Ese recurso ya se encuentra reservado para la fecha y hora de inicio indicados"
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: Horas Incorrectas "
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores
            ListaReservaGeneral.objects.create(recurso_reservado=recurso, estado_reserva='RE',
                                               fecha_reserva=request.POST['fecha_reserva'],
                                               hora_inicio=request.POST['hora_inicio'],
                                               hora_fin=request.POST['hora_fin'])
            if form.is_valid():
                form.save()
            return redirect('reserva:reserva_listar')
    context = {
        'form': form,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/crear_reserva.html', context)


'''Funciones para listar Reservas Especificas Realizadas '''


def reserva_especifica_listar(request):
    """ Funcion que Lista todos los registros creados del modelo de Reservas Generales Especificas
     y los envia al template listar_reserva_especifica.html"""
    qreserva = ReservaEspecifica.objects.all().order_by('reserva_id')
    context = {'reserva': qreserva}
    return render(request, 'reserva/listar_reserva_especifica.html', context)


class ListarReservaEspecifica(ListView):
    model = ReservaGeneral
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

'''Funcion Crear Reserva General '''


def crear_reserva_especifica(request, recurso_id):
    mensaje = None
    if request.method == 'POST':
        form_reserva = ReservaEspecificaForm(request.POST)
        usuario = request.POST.get('profile',)  # Guarda el ide del user, muestra la cedula en el template
        recurso = recurso_id  # Guarda el recurso, en un int, es un selec del nom del recurso
        fecha_reserva = request.POST.get('fecha_reserva',)  # Fecha introducida en el formulario
        hora_inicio = request.POST.get('hora_inicio',)  # Hora de inicio introducida en el formulario
        hora_fin = request.POST.get('hora_fin',)  # Hora fin introducida en el formulario
        reserva = ReservaEspecifica.objects.all()  # No le encontre utilidad aun
        for p in reserva:
            if p.profile == reserva.profile:
                 prioridad = p.profile.categoria
        # Verifica que la fecha no este agendada a la misma hora de inicio
        if verificar_hora_reserva(fecha_reserva, hora_inicio, hora_fin, recurso) == 1:
            mensaje = "Error: Ese recurso ya se encuentra reservado para la fecha y hora de inicio indicados"
        if verificar_hora(hora_inicio, hora_fin) == 1:
            mensaje = "Error: Horas Incorrectas "
        if verificar_estado(recurso) == 1:
            mensaje = "Error: El recurso NO se encuentra 'Disponible' "
        if not mensaje:
            mensaje = 'Reserva Agendada Exitosamente !'  # Guarda en La Lista auxiliar todos los datos anteriores
            ListaReservaEspecifica.objects.create(recurso_reservado=recurso, estado_reserva='SO', prioridad=prioridad,
                                                  fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])

            ReservaGeneral.objects.create(profile_id=request.POST['profile'], recurso_id=recurso, fecha_reserva=request.POST['fecha_reserva'], hora_inicio=request.POST['hora_inicio'], hora_fin=request.POST['hora_fin'])
            return redirect('reserva:reserva_listar')
    else:
        form_reserva = ReservaGeneralForm()
    context = {
        'form': form_reserva,
        'mensaje': mensaje,
    }
    return render(request, 'reserva/crear_reserva.html', context)