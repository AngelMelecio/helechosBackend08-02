from rest_framework import serializers
 
# import the todo data model
from apps.ModeloMaterial.models import ModeloMaterial
from apps.Modelos.models import Modelo
from apps.Materiales.models import Material
from apps.Modelos.serializers import ModeloSerializer
from apps.Materiales.serializers import MaterialSerializerListar
 
class ModeloMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloMaterial
        fields = '__all__'

class ModeloMaterialSerializerListar(serializers.ModelSerializer):
    material = MaterialSerializerListar()
    class Meta:
        model = ModeloMaterial
        fields = '__all__'