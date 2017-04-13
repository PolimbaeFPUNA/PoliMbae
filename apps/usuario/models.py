from __future__ import unicode_literals

from django.db import models


from django.db import models
from django.conf import settings
from  django.contrib.auth.models import User


class UserProfile (models.Model):
    user = models.OneToOneField(User)
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    categoria = models.CharField(max_length=50)
