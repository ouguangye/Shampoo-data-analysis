# Generated by Django 2.2.24 on 2021-10-29 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_auto_20211029_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='序号'),
        ),
    ]