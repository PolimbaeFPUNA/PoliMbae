# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-02 00:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0029_auto_20170530_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 6, 2)),
        ),
    ]
