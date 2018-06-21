# Generated by Django 2.0 on 2018-01-14 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20171225_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='', verbose_name='背景图片')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('created', models.DateField(default='2017-09-15', verbose_name='项目时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='ExhibitionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='名称')),
                ('created', models.DateField(default='2017-09-15', verbose_name='项目时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('picture', models.ImageField(upload_to='', verbose_name='背景图片')),
            ],
        ),
        migrations.AddField(
            model_name='exhibition',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exhibitions', to='home.ExhibitionTag', verbose_name='展会协助'),
        ),
    ]