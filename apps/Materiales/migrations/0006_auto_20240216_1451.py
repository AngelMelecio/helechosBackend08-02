# Generated by Django 3.1.7 on 2024-02-16 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Materiales', '0005_auto_20230404_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='tipo',
            field=models.CharField(choices=[('Poliester', 'Poliester'), ('Melting', 'Melting'), ('Lurex', 'Lurex'), ('Goma', 'Goma'), ('Licra desnuda', 'Licra desnuda'), ('Division', 'Division')], default='Poliester', max_length=20),
        ),
    ]
