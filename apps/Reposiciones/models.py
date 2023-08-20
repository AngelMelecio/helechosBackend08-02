from django.db import models

from apps.Empleados.models import Empleado
from apps.Maquinas.models import Maquina
from apps.Produccion.models import Produccion

class Reposicion(models.Model):
    idReposicion = models.AutoField(auto_created=True, primary_key=True)
    cantidad = models.IntegerField(null=False, blank=False)
    motivos = models.CharField(max_length=500, null=False, blank=True)
    empleadoFalla = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='empleadoFalla')
    empleadoReponedor = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='empleadoReponedor')
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} {} {}".format(self.idReposicion, self.cantidad, self.motivos)

# Create your models here.
