from django.db import models

from apps.FichasTecnicas.models import FichaTecnica
from apps.Materiales.models import Material

# Create your models here.
class FichaTecnicaMaterial(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    guiaHilos = models.CharField(max_length=200,null=True, blank=True)
    hebras = models.IntegerField(null=True,blank=True)
    peso =models.DecimalField(decimal_places=4, max_digits=8)

    def __str__(self):
            return "{} {} {} {}".format(self.fichaTecnica.modelo.nombre+'-',self.fichaTecnica.nombre,self.guiaHilos+'-', self.material)