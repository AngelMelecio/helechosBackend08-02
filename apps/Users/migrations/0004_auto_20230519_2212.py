# Generated by Django 3.1.7 on 2023-05-20 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20230519_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='rol',
            field=models.CharField(choices=[('Encargado', 'Encargado'), ('Desarrollador', 'Desarrollador'), ('Administrador', 'Administrador')], default='Encargado', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.CharField(choices=[('Encargado', 'Encargado'), ('Desarrollador', 'Desarrollador'), ('Administrador', 'Administrador')], default='Encargado', max_length=20),
        ),
    ]
