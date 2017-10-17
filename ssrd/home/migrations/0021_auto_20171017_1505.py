# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20171017_0000'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AlterField(
            model_name='systemdemonstrationpicture',
            name='obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='home.SystemDemonstration'),
        ),
    ]
