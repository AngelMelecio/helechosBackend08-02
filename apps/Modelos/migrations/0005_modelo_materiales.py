# Generated by Django 3.1.7 on 2023-03-15 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0004_modelo_archivoprograma'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo',
            name='materiales',
            field=models.JSONField(default=[]),
        ),
    ]