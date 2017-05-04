# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0016_auto_20170502_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listareservaespecifica',
            name='hora_fin',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listareservaespecifica',
            name='hora_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listareservaespecifica',
            name='prioridad',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='listareservageneral',
            name='hora_fin',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listareservageneral',
            name='hora_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reservaespecifica',
            name='hora_fin',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reservaespecifica',
            name='hora_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reservageneral',
            name='hora_fin',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reservageneral',
            name='hora_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]