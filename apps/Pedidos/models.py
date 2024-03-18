from django.db import models
from apps.Modelos.models import Modelo
# Create your models here.

def valor_por_defecto():
    return {'total': 0, 'progreso': 0,'estado': 'Pendiente'}

class Pedido(models.Model):
    idPedido = models.AutoField(auto_created=True, primary_key=True)
    modelo = models.ForeignKey(
        Modelo, on_delete=models.CASCADE, null=False, blank=False)
    fechaRegistro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fechaEntrega = models.DateField(null=True, blank=True)
    ordenProduccion = models.CharField(max_length=50, null=True, blank=True)
    paresTotales = models.IntegerField(null=False, blank=False, default=0)
    paresProgreso = models.IntegerField(null=False, blank=False, default=0)
    estado = models.CharField(max_length=20,
                            choices=[('Pendiente', 'Pendiente'),('Terminado', 'Terminado'),('Cancelado', 'Cancelado')],
                            default='Pendiente', null=False, blank=False)
    tipo = models.CharField(max_length=20,
                            choices=[('Produccion', 'Produccion'),('Almacen', 'Almacen'),('Muestra', 'Muestra'),('Faltante', 'Faltante'),('Reposicion','Reposicion'),('Otro','Otro')],
                            default='Produccion', null=False, blank=False)
    def __str__(self):
        return "{} {}".format(self.idPedido, self.modelo.nombre)