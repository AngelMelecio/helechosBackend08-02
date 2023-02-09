from django.db import models

# Create your models here.
class Maquina(models.Model):
    idMaquina = models.AutoField(auto_created=True, primary_key=True)
    numero = models.CharField(max_length=50)
    linea = models.CharField(max_length=20,
                            choices=[('0', 'Ninguna'),('1', 'Línea 1'),('2', 'Línea 2'),('3', 'Línea 3')],
                            default='0')
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    ns = models.CharField(max_length=60)
    fechaAdquisicion = models.DateField()
    otros = models.TextField(null=True, blank=True)
    departamento = models.CharField(max_length=20,
                            choices=[('Tejido', 'Tejido'),('Corte', 'Corte'),('Plancha', 'Plancha'),
                                    ('Empaque', 'Empaque'),('Transporte', 'Transporte'),('Diseno', 'Diseño'),('Gerencia', 'Gerencia')],
                            default='Tejido')