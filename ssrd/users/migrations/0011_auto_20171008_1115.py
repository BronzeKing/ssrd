# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 03:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20170927_0041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='真实姓名')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(auto_now=True, verbose_name='生日')),
                ('company', models.CharField(max_length=255, null=True, verbose_name='所属公司')),
                ('position', models.CharField(max_length=255, null=True, verbose_name='职位')),
                ('qq', models.CharField(max_length=20, null=True, verbose_name='QQ号码')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='地址')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together=set([('user',)]),
        ),
    ]
