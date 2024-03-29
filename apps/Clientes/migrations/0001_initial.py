# Generated by Django 3.1.7 on 2023-03-01 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idCliente', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('correo', models.CharField(blank=True, max_length=200, null=True)),
                ('contactos', models.CharField(blank=True, max_length=10000, null=True)),
                ('otro', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
