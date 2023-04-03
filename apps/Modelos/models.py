from django.db import models
from apps.Maquinas.models import Maquina
from apps.Clientes.models import Cliente

def upload_to(instance, filename):
   return 'images/{filename}'.format(filename=filename)



# Create your models here.
class Modelo(models.Model):
   idModelo = models.AutoField(auto_created=True, primary_key=True)
   nombre = models.CharField(max_length=200,null=False, blank=False)
   nombrePrograma = models.CharField(max_length=200,null=False, blank=False)
   archivoPrograma=models.FileField(upload_to=upload_to,null=True, blank=True)
   archivoFichaTecnica=models.FileField(upload_to=upload_to,null=True, blank=True)
   fotografia = models.ImageField(upload_to=upload_to,null=True, blank=True)
   cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING,null=False, blank=False)
   talla = models.CharField(max_length=25,null=False, blank=False)
   maquinaTejido = models.ForeignKey(Maquina, on_delete=models.DO_NOTHING, related_name='maquinaTejido')
   tipoMaquinaTejido = models.CharField(max_length=100,null=True, blank=True)
   galga = models.CharField(max_length=100,null=True, blank=True)
   velocidadTejido = models.CharField(max_length=25,null=False, blank=False)
   tiempoBajada = models.CharField(max_length=25,null=False, blank=False)
   maquinaPlancha = models.ForeignKey(Maquina, on_delete=models.DO_NOTHING, related_name='maquinaPlancha')
   velocidadPlancha = models.CharField(max_length=25,null=False, blank=False)
   temperaturaPlancha = models.CharField(max_length=25,null=False, blank=False)
   materiales = models.JSONField(null=False, blank=False)
   numeroPuntos = models.JSONField(null=True, blank=True)
   jalones = models.JSONField(null=True, blank=True)
   economisadores = models.JSONField(null=True, blank=True)
   otros = models.TextField(null=True, blank=True)

   def __str__(self):
         return "{} {} {}".format(self.nombre, self.talla, self.cliente)