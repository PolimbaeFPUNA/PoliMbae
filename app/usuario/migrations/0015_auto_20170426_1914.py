# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-26 19:14
from __future__ import unicode_literals

import app.rol.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_auto_20170426_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rol',
            field=models.ForeignKey(null=True, on_delete=app.rol.models.UserRol, to='rol.UserRol'),
        ),
    ]
