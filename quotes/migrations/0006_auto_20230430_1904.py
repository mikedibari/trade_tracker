# Generated by Django 3.2.2 on 2023-04-30 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20230430_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='close_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='open_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
