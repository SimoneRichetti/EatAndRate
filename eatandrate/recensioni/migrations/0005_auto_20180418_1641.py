# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-18 16:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recensioni', '0004_auto_20180404_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recensione',
            name='data',
            field=models.DateField(default=datetime.date.today, verbose_name='Data di pubblicazione'),
        ),
    ]
