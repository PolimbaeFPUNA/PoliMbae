# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-01 20:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurso', '0025_auto_20170501_2005'),
        ('mantenimiento', '0007_auto_20170428_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mantenimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega', models.DateTimeField(default=datetime.datetime(2017, 5, 1, 20, 5, 50, 482940, tzinfo=utc))),
                ('fecha_fin', models.DateTimeField(default=datetime.datetime(2017, 5, 1, 20, 5, 50, 482988, tzinfo=utc))),
                ('tipo', models.CharField(blank=True, choices=[('P', 'Preventivo'), ('C', 'Correctivo')], default='', max_length=20)),
                ('resultado', models.CharField(blank=True, choices=[('FUN', 'Funcional'), ('NF', 'No Funcional'), ('PEN', 'Pendiente')], default='', max_length=20)),
                ('recurso', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='recurso.Recurso1')),
                ('tipo_recurso', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='recurso.TipoRecurso1')),
            ],
        ),
    ]