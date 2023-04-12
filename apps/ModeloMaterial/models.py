from django.db import models

from apps.Modelos.models import Modelo
from apps.Materiales.models import Material

# Create your models here.
class ModeloMaterial(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    guiaHilos = models.CharField(max_length=200,null=True, blank=True)
    hebras = models.IntegerField(null=True,blank=True)
    peso =models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
            return "{} {}".format(self.guiaHilos+'-', self.material)