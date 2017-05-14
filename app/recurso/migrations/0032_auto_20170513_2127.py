# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 21:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurso', '0031_auto_20170512_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('ctra_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_caracteristica', models.CharField(max_length=80)),
                ('descripcion', models.CharField(max_length=80)),
                ('activo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Recurso1',
            fields=[
                ('recurso_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_recurso1', models.CharField(max_length=80)),
                ('estado', models.CharField(choices=[('DI', 'Disponible'), ('RE', 'Reservado'), ('EM', 'En Mantenimiento'), ('SO', 'Solicitado'), ('FU', 'Fuera de Uso'), ('EU', 'En Uso')], default='DI', max_length=2)),
                ('recurso_mantenimiento_preventivo', models.DateTimeField(default=django.utils.timezone.now)),
                ('frecuencia_mantenimiento', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoRecurso1',
            fields=[
                ('tipo_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_recurso', models.CharField(max_length=80)),
                ('reservable', models.BooleanField(default=True)),
                ('fecha_mantenimiento', models.DateTimeField(default=django.utils.timezone.now)),
                ('ctra_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.Caracteristica')),
            ],
        ),
        migrations.AddField(
            model_name='recurso1',
            name='tipo_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.TipoRecurso1'),
        ),
    ]
