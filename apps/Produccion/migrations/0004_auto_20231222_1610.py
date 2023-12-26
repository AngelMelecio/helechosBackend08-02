# Generated by Django 3.1.7 on 2023-12-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produccion', '0003_auto_20230803_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='produccion',
            name='destino',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='produccion',
            name='informacionExtra',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='produccion',
            name='tipo',
            field=models.CharField(choices=[('Ordinario', 'Ordinario'), ('Reposicion', 'Reposicion'), ('Extra', 'Extra')], default='Ordinario', max_length=20),
        ),
    ]
