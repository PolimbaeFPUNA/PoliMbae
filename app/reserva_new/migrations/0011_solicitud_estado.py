# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-22 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_new', '0010_auto_20170620_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(choices=[('PEN', 'PEN'), ('RCH', 'RCH')], default='PEN', max_length=3),
        ),
    ]