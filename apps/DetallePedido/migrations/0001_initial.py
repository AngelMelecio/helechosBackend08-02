# Generated by Django 3.1.7 on 2023-06-03 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pedidos', '0001_initial'),
        ('FichasTecnicas', '0004_remove_fichatecnica_nombreprograma'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('idDetallePedido', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('paresPorPaquete', models.IntegerField(blank=True, null=True)),
                ('fichaTecnica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FichasTecnicas.fichatecnica')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pedidos.pedido')),
            ],
        ),
    ]
