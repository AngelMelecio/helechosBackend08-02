# Generated by Django 3.1.7 on 2023-04-13 01:39

import apps.FichasTecnicas.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Maquinas', '0003_auto_20230215_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaTecnica',
            fields=[
                ('idFichaTecnica', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('nombrePrograma', models.CharField(blank=True, max_length=200, null=True)),
                ('archivoPrograma', models.FileField(blank=True, null=True, upload_to=apps.FichasTecnicas.models.upload_to)),
                ('archivoFichaTecnica', models.FileField(blank=True, null=True, upload_to=apps.FichasTecnicas.models.upload_to)),
                ('fotografia', models.ImageField(blank=True, null=True, upload_to=apps.FichasTecnicas.models.upload_to)),
                ('talla', models.CharField(blank=True, max_length=25, null=True)),
                ('tipoMaquinaTejido', models.CharField(blank=True, max_length=100, null=True)),
                ('galga', models.CharField(blank=True, max_length=100, null=True)),
                ('velocidadTejido', models.CharField(blank=True, max_length=25, null=True)),
                ('tiempoBajada', models.CharField(blank=True, max_length=25, null=True)),
                ('velocidadPlancha', models.CharField(blank=True, max_length=25, null=True)),
                ('temperaturaPlancha', models.CharField(blank=True, max_length=25, null=True)),
                ('pesoPoliester', models.CharField(blank=True, max_length=25, null=True)),
                ('pesoMelt', models.CharField(blank=True, max_length=25, null=True)),
                ('pesoLurex', models.CharField(blank=True, max_length=25, null=True)),
                ('numeroPuntos', models.JSONField(blank=True, null=True)),
                ('jalones', models.JSONField(blank=True, null=True)),
                ('economisadores', models.JSONField(blank=True, null=True)),
                ('otros', models.TextField(blank=True, null=True)),
                ('maquinaPlancha', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='maquinaPlancha', to='Maquinas.maquina')),
                ('maquinaTejido', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='maquinaTejido', to='Maquinas.maquina')),
            ],
        ),
    ]
