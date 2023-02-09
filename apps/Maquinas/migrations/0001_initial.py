# Generated by Django 3.1.3 on 2023-01-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('idMaquina', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=50)),
                ('linea', models.CharField(choices=[('0', 'Ninguna'), ('1', 'Línea 1'), ('2', 'Línea 2'), ('3', 'Línea 3')], default='0', max_length=20)),
                ('marca', models.CharField(max_length=60)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('ns', models.CharField(max_length=60)),
                ('fechaAdquisicion', models.DateField()),
                ('otros', models.TextField(blank=True, null=True)),
                ('departamento', models.CharField(choices=[('Tejido', 'Tejido'), ('Corte', 'Corte'), ('Plancha', 'Plancha'), ('Empaque', 'Empaque'), ('Transporte', 'Transporte'), ('Diseno', 'Diseño'), ('Gerencia', 'Gerencia')], default='Tejido', max_length=20)),
            ],
        ),
    ]
