from django.db import models
from apps.DetallePedido.models import DetallePedido
# Create your models here.
class Produccion(models.Model):
    #General
    idProduccion = models.AutoField(auto_created=True, primary_key=True)
    detallePedido = models.ForeignKey(
        DetallePedido, on_delete=models.CASCADE)
    numEtiqueta=models.CharField(max_length=50, null=True, blank=True)
    cantidad=models.IntegerField(null=False, blank=False)
    estacionActual= models.CharField(max_length=50, null=True, blank=True)
    tallaReal= models.CharField(max_length=50, null=False, blank=False)
    fechaImpresion=models.DateTimeField(null=True, blank=True)
    tipo = models.CharField(max_length=20,
                            choices=[('Ordinario', 'Ordinario'),('Reposicion', 'Reposicion'),('Extra', 'Extra')],
                            default='Ordinario', null=False, blank=False)
    destino= models.CharField(max_length=50, null=True, blank=True)
    informacionExtra=models.JSONField(null=True, blank=True)
    contadorRepocision=models.IntegerField(null=False, blank=False,default=0)
    contadorExtra=models.IntegerField(null=False, blank=False,default=0)
    def __str__(self):
        return "{} {} {} {}".format(self.detallePedido.pedido.idPedido,self.tallaReal, self.numEtiqueta ,self.cantidad)
