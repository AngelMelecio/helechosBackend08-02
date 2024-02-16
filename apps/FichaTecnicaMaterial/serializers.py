from rest_framework import serializers
 
# import the todo data model
from apps.FichaTecnicaMaterial.models import FichaTecnicaMaterial
from apps.Materiales.serializers import MaterialSerializerListar,MaterialSerializerGetPedido
 
class FichaTecnicaMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnicaMaterial
        fields = '__all__'

class FichaTecnicaMaterialSerializerListar(serializers.ModelSerializer):
    material = MaterialSerializerListar()
    class Meta:
        model = FichaTecnicaMaterial
        fields = '__all__'

class FichaTecnicaMaterialSerializerListarCorto(serializers.ModelSerializer):
    material = MaterialSerializerListar()
    class Meta:
        model = FichaTecnicaMaterial
        fields = ('id','material','peso')

class FichaMaterialesSerializerGetPedido(serializers.ModelSerializer):
    material = MaterialSerializerGetPedido()
    class Meta:
        model = FichaTecnicaMaterial
        fields = ('id','material')