# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-26 06:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDynamics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='authorizecode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='authorizecode',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='authorizecode',
            name='status',
            field=models.IntegerField(choices=[(-1, '终止'), (0, '停用'), (1, '启用')], default=1, verbose_name='授权码状态'),
        ),
        migrations.AlterField(
            model_name='group',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='项目名称'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(choices=[(1, '用户下订单'), (2, '商务部对接转发'), (3, '设计部上传方案报价'), (4, '领导审核'), (5, '客户审核上传确认'), (6, '商务部审核'), (7, '工程部实施'), (8, '客户签字确认')], default=1, verbose_name='项目状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'ADMIN'), (1, '个人用户'), (2, '行业用户'), (3, '分销商'), (4, '常规用户')], default=1, verbose_name='用户权限'),
        ),
        migrations.AddField(
            model_name='projectdynamics',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectDynamics', to='users.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='collect',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collects', to='users.Project', verbose_name='收藏的项目'),
        ),
        migrations.AddField(
            model_name='collect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collects', to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
    ]
