# Generated by Django 3.1.7 on 2023-08-29 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20230629_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='rol',
            field=models.CharField(choices=[('Encargado', 'Encargado'), ('Desarrollador', 'Desarrollador'), ('Administrador', 'Administrador'), ('Produccion', 'Produccion'), ('Reportes', 'Reportes')], default='Encargado', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.CharField(choices=[('Encargado', 'Encargado'), ('Desarrollador', 'Desarrollador'), ('Administrador', 'Administrador'), ('Produccion', 'Produccion'), ('Reportes', 'Reportes')], default='Encargado', max_length=20),
        ),
    ]
