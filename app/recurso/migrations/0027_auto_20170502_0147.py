# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-02 01:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recurso', '0026_auto_20170501_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiporecurso1',
            name='fecha_mantenimiento',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 2, 1, 47, 20, 984807, tzinfo=utc)),
        ),
    ]
