from django.db import models
from apps.Empleados.models import Empleado
from apps.Maquinas.models import Maquina

# Create your models here.
class EmpleadoMaquina(models.Model):
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    idMaquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)