# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_auto_20171215_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='group',
        ),
        migrations.DeleteModel(
            name='ProjectGroup',
        ),
    ]
