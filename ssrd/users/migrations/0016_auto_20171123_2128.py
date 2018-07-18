# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 13:28
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0015_auto_20171123_1718")]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="content",
            field=django.contrib.postgres.fields.jsonb.JSONField(verbose_name="内容"),
        ),
        migrations.AlterField(
            model_name="projectlog",
            name="content",
            field=django.contrib.postgres.fields.jsonb.JSONField(verbose_name="内容"),
        ),
    ]
