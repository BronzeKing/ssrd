# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 13:54
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20171123_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='content',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='[]', verbose_name='内容'),
        ),
    ]
