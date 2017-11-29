# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 13:44
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_project_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='content',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[], verbose_name='内容'),
        ),
    ]
