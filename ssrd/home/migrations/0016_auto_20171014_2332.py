# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20170923_1802'),
    ]

    operations = [
        migrations.DeleteModel(
            name='System',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
