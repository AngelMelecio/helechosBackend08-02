# Generated by Django 3.1.7 on 2023-06-05 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DetallePedido', '0003_auto_20230605_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='proveedores',
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='colores',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
