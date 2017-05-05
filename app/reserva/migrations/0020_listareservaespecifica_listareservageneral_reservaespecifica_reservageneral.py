# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 04:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurso', '0029_auto_20170505_0459'),
        ('usuario', '0015_auto_20170505_0459'),
        ('reserva', '0019_auto_20170504_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaReservaEspecifica',
            fields=[
                ('lista_id', models.AutoField(primary_key=True, serialize=False)),
                ('recurso_reservado', models.IntegerField()),
                ('estado_reserva', models.CharField(choices=[('DI', 'Disponible'), ('RE', 'Reservado'), ('EM', 'En Mantenimiento'), ('SO', 'Solicitado'), ('FU', 'Fuera de Uso'), ('EU', 'En Uso')], default='DI', max_length=2)),
                ('prioridad', models.IntegerField()),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ListaReservaGeneral',
            fields=[
                ('lista_id', models.AutoField(primary_key=True, serialize=False)),
                ('recurso_reservado', models.IntegerField()),
                ('estado_reserva', models.CharField(choices=[('DI', 'Disponible'), ('RE', 'Reservado'), ('EM', 'En Mantenimiento'), ('SO', 'Solicitado'), ('FU', 'Fuera de Uso'), ('EU', 'En Uso')], default='DI', max_length=2)),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ReservaEspecifica',
            fields=[
                ('reserva_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Profile')),
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.Recurso1')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaGeneral',
            fields=[
                ('reserva_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Profile')),
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso.Recurso1')),
            ],
        ),
    ]
