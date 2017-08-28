# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-27 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170816_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(verbose_name='所属用户')),
                ('title', models.TextField(verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('read', models.SmallIntegerField(choices=[('0', '未读'), ('1', '已读')], default=0, verbose_name='已读')),
                ('rank', models.IntegerField(default=100, verbose_name='排序')),
            ],
        ),
    ]
