# Generated by Django 3.1.2 on 2022-02-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0010_auto_20220128_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='registerDate',
            field=models.DateTimeField(verbose_name='Fecha de registro'),
        ),
    ]