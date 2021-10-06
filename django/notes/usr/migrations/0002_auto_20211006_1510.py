# Generated by Django 3.2.7 on 2021-10-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='creator',
            field=models.CharField(default='Anon', max_length=33),
        ),
        migrations.AlterField(
            model_name='note',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
