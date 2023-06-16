from django.db import models
from apps.Empleados.models import Empleado
from apps.Maquinas.models import Maquina 
from apps.Produccion.models import Produccion

# Create your models here.
class Registro(models.Model):
    idRegistro = models.AutoField(auto_created=True, primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,null=True,blank=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE,null=True,blank=True)
    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE,null=True,blank=True)
    turno = models.CharField(max_length=200,null=True, blank=True)
    fechaCaptura=models.DateTimeField(null=True, blank=True)
    departamento = models.CharField(max_length=20,
                            choices=[('Tejido', 'Tejido'),('Corte', 'Corte'),('Plancha', 'Plancha'),
                                    ('Empaque', 'Empaque'),('Transporte', 'Transporte'),('Diseno', 'Diseño'),('Gerencia', 'Gerencia')],
                            default='Tejido')
    def __str__(self):
        return "{} {}".format(self.departamento, self.fechaCaptura)

