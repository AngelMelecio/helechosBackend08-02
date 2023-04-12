# Generated by Django 3.1.7 on 2023-04-10 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Materiales', '0005_auto_20230404_1101'),
        ('Modelos', '0010_auto_20230404_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guiaHilos', models.CharField(blank=True, max_length=200, null=True)),
                ('hebras', models.IntegerField(blank=True, null=True)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idMaterial', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Materiales.material')),
                ('idModelo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Modelos.modelo')),
            ],
        ),
    ]