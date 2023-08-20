# Generated by Django 3.1.7 on 2023-08-19 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Maquinas', '0003_auto_20230215_2246'),
        ('Produccion', '0003_auto_20230803_1000'),
        ('Empleados', '0002_auto_20230724_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reposicion',
            fields=[
                ('idReposicion', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('motivos', models.CharField(blank=True, max_length=500)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('empleadoFalla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleadoFalla', to='Empleados.empleado')),
                ('empleadoReponedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleadoReponedor', to='Empleados.empleado')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Maquinas.maquina')),
                ('produccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Produccion.produccion')),
            ],
        ),
    ]