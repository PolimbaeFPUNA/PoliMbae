# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 02:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurso', '0022_auto_20170429_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('ctra_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_caracteristica', models.CharField(max_length=80)),
                ('activo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Recurso1',
            fields=[
                ('recurso_id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('DI', 'Disponible'), ('RE', 'Reservado'), ('EM', 'En Mantenimiento'), ('SO', 'Solicitado'), ('FU', 'Fuera de Uso'), ('EU', 'En Uso')], default='DI', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRecurso1',
            fields=[
                ('tipo_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_recurso', models.CharField(max_length=80)),
                ('reservable', models.BooleanField(default=True)),
                ('fecha_mantenimiento', models.DateTimeField(default=datetime.datetime(2017, 5, 1, 2, 32, 16, 937580, tzinfo=utc))),
                ('ctra_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.Caracteristica')),
            ],
        ),
        migrations.AddField(
            model_name='recurso1',
            name='tipo_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.TipoRecurso1'),
        ),
    ]
