from django.db import models

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
    
class Empleado(models.Model):
    idEmpleado = models.AutoField(auto_created=True, primary_key=True)
    fotografia = models.ImageField(upload_to=upload_to, max_length=255, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ns = models.CharField(max_length=16, null=True, blank=True)
    departamento = models.CharField(max_length=20,
                            choices=[('Tejido', 'Tejido'),('Corte', 'Corte'),('Plancha', 'Plancha'),
                                    ('Empaque', 'Empaque'),('Transporte', 'Transporte'),('Diseno', 'Diseño'),('Gerencia', 'Gerencia')],
                            default='Tejido')
    gafete = models.CharField(max_length=200,null=True, blank=True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return "{} {} {}".format(self.nombre, self.apellidos, self.departamento)