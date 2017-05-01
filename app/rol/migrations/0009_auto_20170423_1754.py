# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0008_auto_20170423_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermisoRol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permiso', models.CharField(max_length=150)),
                ('activo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRol',
            fields=[
                ('rol_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=80, unique=True)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='rolusuario',
            name='descripcion',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='rolusuario',
            name='nombre_rol',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='permisorol',
            name='rol_id',
            field=models.ManyToManyField(to='rol.UserRol'),
        ),
    ]
