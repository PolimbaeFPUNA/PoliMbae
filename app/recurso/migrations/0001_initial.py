# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nombre_rec', models.CharField(max_length=50)),
                ('codigo_rec', models.IntegerField(default=0)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
    ]
