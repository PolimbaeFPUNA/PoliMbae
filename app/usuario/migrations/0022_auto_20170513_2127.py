# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 21:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0015_auto_20170513_2127'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0021_auto_20170513_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Institucional', 'Institucional'), ('Titular', 'Titular'), ('Adjunto', 'Adjunto'), ('Asistente', 'Asistente'), ('Encargado de Catedra', 'Encargado de Catedra'), ('Auxiliar de Ensenanza', 'Auxiliar de Ensenanza'), ('Alumno', 'Alumno'), ('Funcionario', 'Funcionario')], default='Funcionario', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(default='', max_length=20)),
                ('direccion', models.CharField(default='', max_length=50)),
                ('telefono', models.CharField(default='', max_length=50)),
                ('categoria', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='usuario.CategoriaUsuario')),
                ('rol', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='rol.UserRol')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
