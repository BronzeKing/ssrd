# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20171025_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='source',
            field=models.SmallIntegerField(choices=[(0, '荣誉资质'), (1, '合作伙伴'), (2, '操作视频'), (3, '文档下载'), (4, '合同'), (5, '签证'), (6, '常用软件'), (7, '设计方案'), (8, '说明文档'), (-1, '全部文档')], verbose_name='来源'),
        ),
    ]
