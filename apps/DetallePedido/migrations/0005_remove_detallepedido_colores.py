# Generated by Django 3.1.7 on 2023-06-22 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DetallePedido', '0004_auto_20230605_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='colores',
        ),
    ]