# Generated by Django 3.1.7 on 2023-08-14 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0003_cliente_rfc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='rfc',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
