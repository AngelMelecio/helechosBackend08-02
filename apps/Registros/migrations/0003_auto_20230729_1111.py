# Generated by Django 3.1.7 on 2023-07-29 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registros', '0002_auto_20230616_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='departamento',
            field=models.CharField(choices=[('Tejido', 'Tejido'), ('Corte', 'Corte'), ('Plancha', 'Plancha'), ('Empaque', 'Empaque'), ('Calidad', 'Calidad'), ('Transporte', 'Transporte'), ('Diseno', 'Diseño'), ('Gerencia', 'Gerencia')], default='Tejido', max_length=20),
        ),
    ]
