from rest_framework import serializers
 
from apps.Materiales.models import Material
from apps.Proveedores.serializers import ProveedorSerializer
 
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialSerializerListar(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()
    class Meta:
        model = Material
        fields = '__all__'