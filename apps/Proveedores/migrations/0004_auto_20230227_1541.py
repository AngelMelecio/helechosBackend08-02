# Generated by Django 3.1.7 on 2023-02-27 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedores', '0003_auto_20230227_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='contactos',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]