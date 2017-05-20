from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.grafico.views import mantenimientos,recursos,reservas

urlpatterns = [

   url(r'^mantenimiento/$', mantenimientos, name='mantenimientos'),
   url(r'^reserva/$', reservas, name='reserva'),
   url(r'^recursos/$', recursos, name='recurso'),

]