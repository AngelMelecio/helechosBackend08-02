# Generated by Django 3.1.7 on 2024-01-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produccion', '0004_auto_20231222_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='produccion',
            name='contadorExtra',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='produccion',
            name='contadorRepocision',
            field=models.IntegerField(default=0),
        ),
    ]
