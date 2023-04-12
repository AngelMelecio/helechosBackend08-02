from django.db import models

#Estructura de un contacto: id, nombre, puesto, correo, telefono
# Create your models here.
class Proveedor(models.Model):
    idProveedor = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=200)
    rfc = models.CharField(max_length=200,null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    telefono = models.CharField(max_length=20,null=True, blank=True)
    correo = models.CharField(max_length=200,null=True, blank=True)
    departamento = models.CharField(max_length=20,
                            choices=[('Tejido', 'Tejido'),('Corte', 'Corte'),('Plancha', 'Plancha'),
                                    ('Empaque', 'Empaque'),('Transporte', 'Transporte'),('Diseno', 'Diseño'),('Gerencia', 'Gerencia')],
                            default='Tejido')
    contactos =models.JSONField(null=True, blank=True)
    otro = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return "{} {}".format(self.nombre, self.rfc)
