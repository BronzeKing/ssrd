# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0020_project_company")]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="linkman",
            field=models.CharField(max_length=50, verbose_name="联系人"),
        ),
        migrations.AlterField(
            model_name="project",
            name="type",
            field=models.CharField(
                choices=[("create", "新建项目"), ("maintain", "故障维护"), ("remove", "迁移、拆除")],
                default=0,
                max_length=20,
                verbose_name="项目类型",
            ),
        ),
    ]
