# Generated by Django 2.0.1 on 2018-06-20 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0048_auto_20180620_1452")]

    operations = [
        migrations.AlterUniqueTogether(
            name="directory", unique_together={("parent", "name")}
        ),
        migrations.AlterUniqueTogether(
            name="media", unique_together={("directory", "name")}
        ),
    ]
