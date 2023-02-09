from rest_framework import serializers
 
# import the todo data model
from apps.EmpleadoMaquina.models import EmpleadoMaquina
from apps.Empleados.models import Empleado
from apps.Maquinas.models import Maquina
 
 
# create a serializer class
class EmpleadoMaquinaSerializer(serializers.ModelSerializer):
    

    # create a meta class
    class Meta:
        model = EmpleadoMaquina
        fields = '__all__'