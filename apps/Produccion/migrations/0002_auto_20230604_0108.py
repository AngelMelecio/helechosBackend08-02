# Generated by Django 3.1.7 on 2023-06-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produccion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='capturaCalidad',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='capturaCorte',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='capturaEmpaque',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='capturaEntrega',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='capturaPlancha',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='capturaTejido',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]