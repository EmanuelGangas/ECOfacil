# Generated by Django 3.2.18 on 2023-06-01 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ventas', '0002_ventas_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ventas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.ventas')),
            ],
        ),
    ]