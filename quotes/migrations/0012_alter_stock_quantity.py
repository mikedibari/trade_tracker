# Generated by Django 3.2.2 on 2023-05-03 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0011_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
