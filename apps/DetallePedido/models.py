from django.db import models

from apps.FichasTecnicas.models import FichaTecnica
from apps.Pedidos.models import Pedido

# Create your models here.
class DetallePedido(models.Model):
    idDetallePedido = models.AutoField(auto_created=True, primary_key=True)
    fichaTecnica = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidades = models.JSONField(null=True,blank=True)
    rutaProduccion= models.JSONField(null=True, blank=True)
    
    def __str__(self):
            return "{} {}".format(self.pedido.idPedido,self.fichaTecnica.talla)