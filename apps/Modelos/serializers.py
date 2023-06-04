from rest_framework import serializers
from apps.Modelos.models import Modelo
from apps.Clientes.serializers import ClienteSerializerSimple

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class ModeloSerializerListar(serializers.ModelSerializer):
    cliente = ClienteSerializerSimple()
    class Meta:
        model = Modelo
        fields = '__all__'