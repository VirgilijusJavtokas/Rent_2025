# Generated by Django 5.1.6 on 2025-03-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0024_reservation_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['-pk'], 'verbose_name': 'Produkto būsena', 'verbose_name_plural': 'Produktų būsenos'},
        ),
        migrations.AlterField(
            model_name='status',
            name='condition',
            field=models.CharField(blank=True, choices=[('n', 'Laikinai neprieinama'), ('i', 'Išnuomota'), ('g', 'Prekę turime sandėlyje.'), ('r', 'Rezervuota')], default='a', max_length=1, verbose_name='Būsena'),
        ),
    ]
