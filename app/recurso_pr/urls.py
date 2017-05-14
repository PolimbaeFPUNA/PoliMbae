from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.recurso_pr.views import *
from django.contrib.auth.decorators import login_required,permission_required

urlpatterns = [

   url(r'^crear/$', crear_tipo_recurso, name='recurso_pr_crear'),
   url(r'^crearrecurso/$', crear_recurso, name='recurso_pr_crear_recurso'),

]