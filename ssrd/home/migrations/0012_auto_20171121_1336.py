# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("home", "0011_auto_20171121_1121")]

    operations = [
        migrations.AddField(
            model_name="news",
            name="updated",
            field=models.DateTimeField(auto_now=True, verbose_name="更新时间"),
        ),
        migrations.AlterField(
            model_name="news",
            name="type",
            field=models.SmallIntegerField(
                choices=[(0, "全部新闻"), (1, "公司新闻"), (2, "公益咨询"), (3, "咨询文章")],
                default=1,
                verbose_name="类型",
            ),
        ),
    ]
