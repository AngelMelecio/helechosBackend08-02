# Generated by Django 3.1.7 on 2023-03-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0005_modelo_materiales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo',
            name='materiales',
            field=models.JSONField(),
        ),
    ]