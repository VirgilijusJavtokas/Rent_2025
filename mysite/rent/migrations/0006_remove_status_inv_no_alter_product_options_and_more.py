# Generated by Django 5.1.6 on 2025-03-03 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0005_alter_status_options_remove_status_warehouse_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='inv_no',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['inv_no'], 'verbose_name': 'Prouktas', 'verbose_name_plural': 'Produktai'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['product'], 'verbose_name': 'Produkto būsena', 'verbose_name_plural': 'Produktų būsenos'},
        ),
        migrations.AddField(
            model_name='product',
            name='inv_no',
            field=models.CharField(blank=True, help_text='Veskite invenorizacijos numerį', max_length=100, null=True, unique=True, verbose_name='Invenorizacijos numeris'),
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]
