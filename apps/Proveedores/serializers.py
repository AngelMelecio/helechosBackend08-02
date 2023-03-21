from rest_framework import serializers
 
# import the todo data model
from apps.Proveedores.models import Proveedor
 

# create a serializer class
class ProveedorSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Proveedor
        fields = '__all__'
