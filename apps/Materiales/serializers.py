from rest_framework import serializers
 
from apps.Materiales.models import Material
from apps.Proveedores.serializers import ProveedorSerializerSimple
 
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialSerializerListar(serializers.ModelSerializer):
    proveedor = ProveedorSerializerSimple()
    class Meta:
        model = Material
        fields = '__all__'

class MaterialSerializerGetPedido(serializers.ModelSerializer):
    proveedor = ProveedorSerializerSimple()
    class Meta:
        model = Material
        fields = ('proveedor','color','tenida','codigoColor','tipo')