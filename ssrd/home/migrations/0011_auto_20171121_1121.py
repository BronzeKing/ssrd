# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_aboutus_fax'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='tel',
            field=models.CharField(default='', max_length=20, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='postcode',
            field=models.CharField(max_length=10, verbose_name='邮编'),
        ),
    ]