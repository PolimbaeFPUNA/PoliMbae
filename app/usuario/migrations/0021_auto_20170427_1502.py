# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-27 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0020_auto_20170427_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rol',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='rol.UserRol'),
        ),
    ]
