from django.db import models
from apps.Clientes.models import Cliente

# Create your models here.
class Modelo(models.Model):
    idModelo = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return "{} {}".format(self.nombre, self.cliente)
