# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 06:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20171121_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Group'),
        ),
    ]
