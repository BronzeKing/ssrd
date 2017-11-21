# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 06:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20171121_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='group',
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.Group'),
        ),
    ]