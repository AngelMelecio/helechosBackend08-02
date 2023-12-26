from django.db import models

class TipoMaterial(models.Model):
    idTipoMaterial = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.nombre)
    