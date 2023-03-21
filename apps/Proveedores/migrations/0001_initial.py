# Generated by Django 3.1.7 on 2023-02-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('idProveedor', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=200)),
                ('otro', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
