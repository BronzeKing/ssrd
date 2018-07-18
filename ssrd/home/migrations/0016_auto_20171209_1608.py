# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 08:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("home", "0015_auto_20171128_1630")]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="产品类别")),
                (
                    "parent_id",
                    models.IntegerField(blank=True, null=True, verbose_name="父级目录"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
            ],
        ),
        migrations.RemoveField(model_name="product", name="domain"),
        migrations.RemoveField(model_name="product", name="other"),
        migrations.RemoveField(model_name="product", name="summary"),
        migrations.RemoveField(model_name="product", name="techParameter"),
        migrations.AddField(
            model_name="product",
            name="content",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=[], verbose_name="产品内容"
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="type",
            field=models.SmallIntegerField(
                choices=[
                    (0, "全部新闻"),
                    (4, "首页公告"),
                    (1, "公司新闻"),
                    (2, "公益咨询"),
                    (3, "咨询文章"),
                ],
                default=1,
                verbose_name="类型",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="home.Category",
                verbose_name="产品分类",
            ),
        ),
        migrations.DeleteModel(name="ProductCategory"),
    ]
