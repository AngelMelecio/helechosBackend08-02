# Generated by Django 3.1.7 on 2023-05-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0002_modelo_fechacreacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
