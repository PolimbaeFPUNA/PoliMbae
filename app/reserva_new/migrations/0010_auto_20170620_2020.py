# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-21 00:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_new', '0009_reserva_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_reserva',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='hora_fin',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='hora_inicio',
            field=models.TimeField(),
        ),
    ]