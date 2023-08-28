# Generated by Django 3.1.7 on 2023-08-22 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0002_auto_20230724_1025'),
        ('Maquinas', '0003_auto_20230215_2246'),
        ('Reposiciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reposicion',
            name='empleadoFalla',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleadoFalla', to='Empleados.empleado'),
        ),
        migrations.AlterField(
            model_name='reposicion',
            name='maquina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Maquinas.maquina'),
        ),
    ]
