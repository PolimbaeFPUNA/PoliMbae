# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 19:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurso_pr', '0005_auto_20170602_1942'),
        ('usuario', '0033_auto_20170602_1942'),
        ('reserva', '0031_listareservaespecifica_listareservageneral_reservaespecifica_reservageneral'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaReservaEspecifica',
            fields=[
                ('lista_id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(default='', max_length=20)),
                ('recurso_reservado', models.IntegerField()),
                ('estado_reserva', models.CharField(choices=[('DI', 'Disponible'), ('RE', 'Reservado'), ('EM', 'En Mantenimiento'), ('SO', 'Solicitado'), ('FU', 'Fuera de Uso'), ('EU', 'En Uso')], default='DI', max_length=2)),
                ('prioridad', models.CharField(default='', max_length=20)),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ListaReservaGeneral',
            fields=[
                ('lista_id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(default='', max_length=20)),
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
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso_pr.Recurso1')),
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
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso_pr.Recurso1')),
            ],
        ),
    ]