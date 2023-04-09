from rest_framework import serializers
 
from apps.Modelos.models import Modelo
from apps.Clientes.serializers import ClienteSerializer
from apps.Maquinas.serializers import MaquinaSerializer

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class ModeloSerializerListar(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    maquinaTejido = MaquinaSerializer()
    maquinaPlancha = MaquinaSerializer()
    class Meta:
        model = Modelo
        fields = '__all__'