# Generated by Django 3.1.7 on 2023-05-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FichasTecnicas', '0006_auto_20230520_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichatecnica',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='fichatecnica',
            name='fechaUltimaEdicion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
