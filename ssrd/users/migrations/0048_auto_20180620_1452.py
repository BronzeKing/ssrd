# Generated by Django 2.0.1 on 2018-06-20 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_directory_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dirs', to='users.Directory'),
        ),
        migrations.AlterField(
            model_name='media',
            name='directory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='users.Directory'),
        ),
        migrations.AlterField(
            model_name='media',
            name='name',
            field=models.CharField(default='', max_length=512, verbose_name='文件名'),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('create', '新建项目'), ('maintain', '故障维护'), ('remove', '迁移、拆除'), ('exhibition', '展会协助')], default='create', max_length=20, verbose_name='项目类型'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(choices=[(0, '管理员'), (1, '经理'), (2, '成员'), (10, '个人用户'), (11, '常规用户'), (12, '行业用户'), (13, '分销商')], default=2, verbose_name='用户权限'),
        ),
    ]
