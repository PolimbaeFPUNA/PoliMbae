# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0028_auto_20170530_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriausuario',
            name='nombre',
            field=models.CharField(choices=[('Institucional', 'Institucional'), ('Titular', 'Titular'), ('Adjunto', 'Adjunto'), ('Asistente', 'Asistente'), ('Encargado de Catedra', 'Encargado de Catedra'), ('Auxiliar de Ensenanza', 'Auxiliar de Ensenanza'), ('Alumno', 'Alumno'), ('Funcionario', 'Funcionario')], default='Funcionario', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='categoria',
            field=models.CharField(choices=[('Institucional', 'Institucional'), ('Titular', 'Titular'), ('Adjunto', 'Adjunto'), ('Asistente', 'Asistente'), ('Encargado de Catedra', 'Encargado de Catedra'), ('Auxiliar de Ensenanza', 'Auxiliar de Ensenanza'), ('Alumno', 'Alumno'), ('Funcionario', 'Funcionario')], default='Funcionario', max_length=30),
        ),
    ]