# Generated by Django 3.1.7 on 2023-06-16 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DetallePedido', '0004_auto_20230605_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produccion',
            fields=[
                ('idProduccion', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('numEtiqueta', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('estacionActual', models.CharField(blank=True, max_length=50, null=True)),
                ('tallaReal', models.CharField(max_length=50)),
                ('fechaImpresion', models.DateTimeField(blank=True, null=True)),
                ('detallePedido', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='DetallePedido.detallepedido')),
            ],
        ),
    ]
