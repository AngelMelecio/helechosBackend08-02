from django.db import models
from apps.Maquinas.models import Maquina
from apps.DetallePedido.models import DetallePedido
from apps.Empleados.models import Empleado

# Create your models here.
class Produccion(models.Model):
    #General
    idProduccion = models.AutoField(auto_created=True, primary_key=True)
    detallePedido = models.ForeignKey(
        DetallePedido, on_delete=models.DO_NOTHING)
    numEtiqueta=models.IntegerField(null=False, blank=False)
    cantidad=models.IntegerField(null=False, blank=False)
    estacionActual= models.JSONField(null=False, blank=False)
    #Tejido
    tejido =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaTejido = models.DateTimeField(null=True, blank=True)
    tejedor = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='tejedor',null=True, blank=True)
    maquinaTejidoProduccion = models.ForeignKey(
        Maquina, on_delete=models.DO_NOTHING, related_name='maquinaTejidoProduccion',null=True, blank=True)
    turnoTejido = models.CharField(max_length=50, null=True, blank=True)
    #Plancha
    plancha =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaPlancha = models.DateTimeField(null=True, blank=True)
    planchador = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='planchador',null=True, blank=True)
    maquinaPlanchaProduccion = models.ForeignKey(
        Maquina, on_delete=models.DO_NOTHING, related_name='maquinaPlanchaProduccion',null=True, blank=True)
    turnoPlancha = models.CharField(max_length=50, null=True, blank=True)   
    #Corte
    corte =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaCorte = models.DateTimeField(null=True, blank=True)
    cortador = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='cortador',null=True, blank=True)
    maquinaCorteProduccion = models.ForeignKey(
        Maquina, on_delete=models.DO_NOTHING, related_name='maquinaCorteProduccion',null=True, blank=True)
    turnoCorte = models.CharField(max_length=50, null=True, blank=True)  
    #Calidad
    calidad =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaCalidad = models.DateTimeField(null=True, blank=True)
    inspector = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='inspector',null=True, blank=True)
    turnoCalidad = models.CharField(max_length=50, null=True, blank=True) 
    #Empaque
    empaque =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaEmpaque = models.DateTimeField(null=True, blank=True)
    empacador = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='empacador',null=True, blank=True)
    turnoEmpaque = models.CharField(max_length=50, null=True, blank=True) 
    stante = models.CharField(max_length=50, null=True, blank=True)
    #Entrega
    entrega =  models.CharField(max_length=5,
                            choices=[('-1', '-1'),('0', '0'),('1', '1')],
                            default='-1') 
    capturaEntrega = models.DateTimeField(null=True, blank=True)
    repartidor = models.ForeignKey(
        Empleado, on_delete=models.DO_NOTHING, related_name='repartidor',null=True, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.detallePedido.fichaTecnica.talla, self.numEtiqueta ,self.cantidad)
