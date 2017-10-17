# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20171017_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='产品名称')),
                ('description', models.TextField(verbose_name='产品描述')),
                ('summary', models.TextField(verbose_name='产品概述')),
                ('techParameter', models.TextField(verbose_name='技术参数')),
                ('domain', models.TextField(verbose_name='应用领域')),
                ('other', models.TextField(verbose_name='其他')),
                ('background', models.ImageField(upload_to='', verbose_name='背景图片')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ProductCategory', verbose_name='产品分类')),
            ],
        ),
    ]
