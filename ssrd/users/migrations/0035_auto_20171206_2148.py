# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0034_auto_20171206_2145")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="mobile",
            field=models.CharField(
                max_length=11, unique=True, verbose_name="Mobile Phone"
            ),
        ),
    ]
