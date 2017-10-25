# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_delete_systemcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('description', models.TextField(verbose_name='描述')),
                ('address', models.CharField(max_length=100, verbose_name='工程地址')),
                ('content', models.TextField(verbose_name='工程内容')),
                ('picture', models.ImageField(upload_to='', verbose_name='背景图片')),
                ('created', models.DateField(default='2017-09-15', verbose_name='项目时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('system', models.ManyToManyField(to='home.System', verbose_name='系统')),
            ],
        ),
        migrations.CreateModel(
            name='SystemCasePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='图片')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='home.SystemCase')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
