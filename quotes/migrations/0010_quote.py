# Generated by Django 3.2.2 on 2023-05-01 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_auto_20230430_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('previous_close', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('ytd_change', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('week_52_high', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('week_52_low', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
            ],
        ),
    ]
