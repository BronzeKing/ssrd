# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-26 16:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ssrd.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170927_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizeCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=ssrd.users.models.generate_key, max_length=40, verbose_name='授权码')),
                ('status', models.SmallIntegerField(choices=[(-1, '终止'), (0, '停用'), (1, '启用')], default=1, verbose_name='授权码状态')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authorizecodes', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authorizecode', to=settings.AUTH_USER_MODEL, verbose_name='授权码对应用户')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=ssrd.users.models.generate_key, max_length=40, verbose_name='邀请码')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL, verbose_name='邀请码所属用户')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invitation', to=settings.AUTH_USER_MODEL, verbose_name='受邀用户')),
            ],
        ),
    ]