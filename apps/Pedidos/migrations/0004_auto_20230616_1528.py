# Generated by Django 3.1.7 on 2023-06-16 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0003_auto_20230607_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fechaRegistro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]