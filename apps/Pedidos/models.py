from django.db import models
from apps.Modelos.models import Modelo
# Create your models here.

class Pedido(models.Model):
    idPedido = models.AutoField(auto_created=True, primary_key=True)
    modelo = models.ForeignKey(
        Modelo, on_delete=models.CASCADE, null=False, blank=False)
    fechaRegistro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fechaEntrega = models.DateField(null=True, blank=True)
    ordenCompra = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return "{} {}".format(self.idPedido, self.modelo.nombre)