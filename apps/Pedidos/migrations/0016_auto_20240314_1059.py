# Generated by Django 3.1.7 on 2024-03-14 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0015_renombrar_campo_ordenCompra_ordenProduccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Terminado', 'Terminado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20),
        ),
    ]
