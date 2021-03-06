# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-24 23:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('underTheaterApp', '0006_classtheater'),
    ]

    operations = [
        migrations.AddField(
            model_name='classtheater',
            name='owner',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='due\xf1o de la publicacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classtheater',
            name='teacher',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='underTheaterApp.Actor', verbose_name='teacher'),
            preserve_default=False,
        ),
    ]
