# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-24 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recurso_pr', '0007_auto_20170623_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurso1',
            name='frecuencia',
        ),
        migrations.AddField(
            model_name='tiporecurso1',
            name='frecuencia',
            field=models.CharField(default='', max_length=3),
        ),
    ]
