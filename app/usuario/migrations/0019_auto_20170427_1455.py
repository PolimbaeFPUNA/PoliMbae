# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-27 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0010_auto_20170424_0330'),
        ('usuario', '0018_auto_20170427_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='rol',
        ),
        migrations.AddField(
            model_name='profile',
            name='rol',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='rol.UserRol'),
        ),
    ]