# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_aboutus'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='fax',
            field=models.CharField(default='', max_length=20, verbose_name='传真'),
        ),
    ]
