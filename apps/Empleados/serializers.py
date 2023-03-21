from rest_framework import serializers,viewsets
 
# import the todo data model
from apps.Empleados.models import Empleado
 

# create a serializer class
class EmpleadoSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Empleado
        fields = '__all__'
