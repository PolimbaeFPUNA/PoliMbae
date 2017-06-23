from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from app.usuario.models import Profile
# Create your models here.



class Log(models.Model):

    usuario= models.ForeignKey(User)
    fecha_hora= models.DateTimeField()
    mensaje= models.TextField()