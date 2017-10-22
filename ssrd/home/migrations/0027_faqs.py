# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_delete_faqs'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questioin', models.TextField(verbose_name='问题')),
                ('answer', models.TextField(verbose_name='回答')),
                ('rank', models.IntegerField(default=100, verbose_name='排序')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]