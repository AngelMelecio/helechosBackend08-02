# Generated by Django 3.1.7 on 2023-03-14 15:09

import apps.Modelos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0003_auto_20230301_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo',
            name='archivoPrograma',
            field=models.FileField(blank=True, null=True, upload_to=apps.Modelos.models.upload_to),
        ),
    ]
