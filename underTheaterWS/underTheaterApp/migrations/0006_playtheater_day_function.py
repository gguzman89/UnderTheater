# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('underTheaterApp', '0005_auto_20160924_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='playtheater',
            name='day_function',
            field=models.ManyToManyField(to='underTheaterApp.DayFunction', verbose_name='dia de funcion'),
        ),
    ]