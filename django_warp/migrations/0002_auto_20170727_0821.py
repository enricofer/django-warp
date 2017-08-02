# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-27 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_warp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasets',
            name='extentBottom',
            field=models.FloatField(default='-8000000.00'),
        ),
        migrations.AlterField(
            model_name='datasets',
            name='extentLeft',
            field=models.FloatField(default='-18000000.00'),
        ),
        migrations.AlterField(
            model_name='datasets',
            name='extentRight',
            field=models.FloatField(default='2000000.00'),
        ),
        migrations.AlterField(
            model_name='datasets',
            name='extentTop',
            field=models.FloatField(default='15000000.00'),
        ),
    ]
