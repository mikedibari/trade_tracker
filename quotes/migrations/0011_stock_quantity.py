# Generated by Django 3.2.2 on 2023-05-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0010_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]
