from django.shortcuts import render
from models import Log

# Create your views here.
def listar_log(request):
    """ Funcion que maneja la vista del listado de Reservas.
    1- La lista despliega las reservas que se confirman en la fecha de hoy al momento en que llega.
    2- Solo se listan las reservas cuyo estado es CONFIRMADA y EN CURSO"""
    logs= Log.objects.all()
    context = {'logs': logs}
    return render(request, 'log/listar_log.html', context)