# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 09:46
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171106_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='content',
            field=jsonfield.fields.JSONField(verbose_name='内容'),
        ),
    ]