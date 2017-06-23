from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required,permission_required
from app.log.views import *
''' Listado de todas las urls secundarias de la url global /recurso/'''

urlpatterns = [

    url(r'^listar_log/', permission_required('log.add_log')(listar_log), name='log_listar'),

]