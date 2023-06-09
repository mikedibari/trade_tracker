# Generated by Django 3.2.2 on 2023-04-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='buy_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='close_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='open_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='sell_price',
            field=models.FloatField(null=True),
        ),
    ]
