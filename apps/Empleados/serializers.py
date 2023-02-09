from rest_framework import serializers
 
# import the todo data model
from apps.Empleados.models import Empleado
 
# create a serializer class
class EmpleadoSerializer(serializers.ModelSerializer):
 
    image_url = serializers.ImageField(required=False)

    # create a meta class
    class Meta:
        model = Empleado
        fields = '__all__'