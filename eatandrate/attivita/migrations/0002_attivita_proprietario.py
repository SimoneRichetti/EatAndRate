# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('attivita', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attivita',
            name='proprietario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.OwnerProfile'),
        ),
    ]
