from django.db import models
from apps.Proveedores.models import Proveedor
#Agregar campo de ficha tecnica pdf al modelo
# Create your models here.
class Material(models.Model):
    idMaterial = models.AutoField(auto_created=True, primary_key=True)
    tipo =  models.CharField(max_length=20,
                            choices=[('Poliester', 'Poliester'),('Melting', 'Melting'),('Lurex', 'Lurex'),('Goma','Goma'),('Licra desnuda','Licra desnuda')],
                            default='Poliester') 
    color= models.CharField(max_length=200,null=True, blank=True)
    calibre= models.CharField(max_length=5,
                              choices=[('150', '150'),('300', '300')],null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    tenida = models.CharField(max_length=200,null=True, blank=True)
    codigoColor = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return "{} {} {}".format(self.tipo, self.color, self.proveedor)  