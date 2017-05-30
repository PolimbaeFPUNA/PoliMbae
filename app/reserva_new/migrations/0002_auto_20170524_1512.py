# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0025_auto_20170516_0158'),
        ('recurso_pr', '0003_auto_20170516_0158'),
        ('reserva_new', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('lista_id', models.AutoField(primary_key=True, serialize=False)),
                ('estado_reserva', models.CharField(choices=[('CONFIRMADA', 'Confirmada'), ('CANCELADA', 'Cancelada')], max_length=2)),
                ('fecha_reserva', models.DateField(default=django.utils.timezone.now)),
                ('hora_inicio', models.TimeField(default=django.utils.timezone.now)),
                ('hora_fin', models.TimeField(default=django.utils.timezone.now)),
                ('recurso_reservado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recurso_pr.Recurso1')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Profile')),
            ],
        ),
        migrations.DeleteModel(
            name='ListaSolicitudEspecifica',
        ),
    ]
