# Generated by Django 3.1.7 on 2023-02-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maquinas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='detallesAdquisicion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
