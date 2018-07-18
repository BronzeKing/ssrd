# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("home", "0018_auto_20171209_1637")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="home.Category",
                verbose_name="产品分类",
            ),
        )
    ]
