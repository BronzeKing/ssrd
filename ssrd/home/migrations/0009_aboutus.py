# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_delete_aboutus'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduction', models.TextField(verbose_name='简介')),
                ('culture', models.TextField(verbose_name='企业文化')),
                ('address', models.CharField(max_length=100, verbose_name='联系地址')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('postcode', models.CharField(max_length=20, verbose_name='电话')),
            ],
        ),
    ]