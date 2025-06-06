# Generated by Django 5.1.6 on 2025-03-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0026_remove_status_is_available_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='approval_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Patvirtinimo data'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_approved',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Ar patvirtinta'),
        ),
        migrations.AddField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Sukurta'),
        ),
    ]
