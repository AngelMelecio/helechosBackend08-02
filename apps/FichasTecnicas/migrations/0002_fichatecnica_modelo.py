# Generated by Django 3.1.7 on 2023-04-13 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Modelos', '0001_initial'),
        ('FichasTecnicas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichatecnica',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='modelo', to='Modelos.modelo'),
        ),
    ]
