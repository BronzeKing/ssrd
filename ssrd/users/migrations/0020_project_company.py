# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.CharField(max_length=255, null=True, verbose_name='所属公司'),
        ),
    ]
