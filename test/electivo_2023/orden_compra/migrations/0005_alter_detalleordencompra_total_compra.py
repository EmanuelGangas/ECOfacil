# Generated by Django 3.2.18 on 2023-06-12 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden_compra', '0004_detalleordencompra_total_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleordencompra',
            name='total_compra',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]
