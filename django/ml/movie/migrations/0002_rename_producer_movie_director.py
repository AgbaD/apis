# Generated by Django 3.2.7 on 2021-10-10 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='producer',
            new_name='director',
        ),
    ]