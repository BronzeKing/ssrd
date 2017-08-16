# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-16 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170726_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharityActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='文章主题')),
                ('content', models.TextField(verbose_name='文章内容')),
            ],
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='Recruitment',
        ),
        migrations.RemoveField(
            model_name='product',
            name='picture',
        ),
        migrations.AlterField(
            model_name='faqs',
            name='rank',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.ProductCategory', verbose_name='产品类别'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='产品名称'),
        ),
        migrations.RemoveField(
            model_name='recruitment',
            name='category',
        ),
        migrations.AddField(
            model_name='recruitment',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.RecruitmentCategory', verbose_name='职位类别'),
        ),
        migrations.AlterField(
            model_name='servicenet',
            name='address',
            field=models.CharField(max_length=100, verbose_name='联系地址'),
        ),
        migrations.AlterField(
            model_name='servicenet',
            name='linkman',
            field=models.CharField(max_length=50, verbose_name='联系人'),
        ),
        migrations.AlterField(
            model_name='servicenet',
            name='mobile',
            field=models.IntegerField(verbose_name='联系手机'),
        ),
        migrations.AlterField(
            model_name='servicenet',
            name='name',
            field=models.CharField(max_length=50, verbose_name='网点名称'),
        ),
        migrations.AlterField(
            model_name='servicenet',
            name='rank',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='servicepromise',
            name='rank',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
    ]
