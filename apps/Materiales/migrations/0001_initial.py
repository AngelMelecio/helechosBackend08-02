# Generated by Django 3.1.7 on 2023-03-01 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Proveedores', '0005_auto_20230301_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('idMaterial', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('Políester', 'Poliester'), ('Melting', 'Melting'), ('Lurex', 'Lurex'), ('Goma', 'Goma'), ('Licra desnuda', 'Licra desnuda')], default='Políester', max_length=20)),
                ('color', models.CharField(max_length=200)),
                ('calibre', models.CharField(choices=[('150', '150'), ('300', '300')], max_length=5)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Proveedores.proveedor')),
            ],
        ),
    ]
