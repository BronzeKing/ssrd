# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 06:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_product_system_systemcase'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='Documents',
        ),
    ]