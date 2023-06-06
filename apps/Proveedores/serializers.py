from rest_framework import serializers
 
# import the todo data model
from apps.Proveedores.models import Proveedor
 

# create a serializer class
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('idProveedor','nombre')

