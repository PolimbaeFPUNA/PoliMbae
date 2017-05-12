from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.grafico.views import *

urlpatterns = [

   url(r'^mantenimiento/$', login_required(mantenimientos), name='mantenimientos'),
   url(r'^reserva/$', login_required(reservas), name='reserva'),
   url(r'^recursos/$', login_required(recursos), name='recurso'),

]