from django.db import models
from apps.Maquinas.models import Maquina
from apps.Modelos.models import Modelo


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


# Create your models here.
class FichaTecnica(models.Model):
    idFichaTecnica = models.AutoField(auto_created=True, primary_key=True)
    modelo = models.ForeignKey(
        Modelo, on_delete=models.DO_NOTHING, related_name='modelo')
    nombre = models.CharField(max_length=200, null=True, blank=True)
    nombrePrograma = models.CharField(
        max_length=100, null=True, blank=True)
    fotografia = models.ImageField(upload_to=upload_to, null=True, blank=True)
    talla = models.CharField(max_length=25, null=True, blank=True)
    maquinaTejido = models.ForeignKey(
        Maquina, on_delete=models.DO_NOTHING, related_name='maquinaTejido')
    tipoMaquinaTejido = models.CharField(max_length=100, null=True, blank=True)
    galga = models.CharField(max_length=100, null=True, blank=True)
    velocidadTejido = models.CharField(max_length=25, null=True, blank=True)
    tiempoBajada = models.CharField(max_length=25, null=True, blank=True)
    maquinaPlancha = models.ForeignKey(
        Maquina, on_delete=models.DO_NOTHING, related_name='maquinaPlancha')
    velocidadPlancha = models.CharField(max_length=25, null=True, blank=True)
    temperaturaPlancha = models.CharField(max_length=25, null=True, blank=True)
    numeroPuntos = models.JSONField(null=True, blank=True)
    jalones = models.JSONField(null=True, blank=True)
    economisadores = models.JSONField(null=True, blank=True)
    otros = models.TextField(null=True, blank=True)
    fechaCreacion = models.DateTimeField( auto_now_add=True, null=True, blank=True)
    fechaUltimaEdicion = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.idFichaTecnica,self.modelo ,self.nombre)
