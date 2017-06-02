# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-01 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_new', '0005_auto_20170601_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='estado_reserva',
            field=models.CharField(choices=[('CONFIRMADA', 'CONFIRMADA'), ('CANCELADA', 'CANCELADA'), ('EN CURSO', 'EN CURSO')], max_length=20),
        ),
    ]
