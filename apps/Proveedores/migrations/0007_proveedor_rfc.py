# Generated by Django 3.1.7 on 2023-04-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedores', '0006_auto_20230301_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='rfc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]