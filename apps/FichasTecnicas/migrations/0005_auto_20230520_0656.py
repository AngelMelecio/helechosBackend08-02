# Generated by Django 3.1.7 on 2023-05-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FichasTecnicas', '0004_remove_fichatecnica_nombreprograma'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fichatecnica',
            name='archivoPrograma',
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='nombrePrograma',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
