# Generated by Django 3.2.7 on 2021-10-13 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_auto_20211013_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='user_id',
            field=models.IntegerField(verbose_name=1),
        ),
    ]
