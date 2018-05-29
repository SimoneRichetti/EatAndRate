# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recensioni', '0002_auto_20180331_1051'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risposta', models.TextField(max_length=256, verbose_name='risposta')),
                ('visualizzata', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualizzata', models.BooleanField(default=False)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.OwnerProfile', verbose_name='destinatario')),
                ('mittente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='mittente')),
                ('recensione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recensioni.Recensione', verbose_name='recensione')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='notifica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification', verbose_name='notifica originale'),
        ),
    ]