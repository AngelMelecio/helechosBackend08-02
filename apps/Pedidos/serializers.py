from rest_framework import serializers
from apps.Pedidos.models import Pedido
from apps.Modelos.serializers import ModeloSerializerListar

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoSerializerListar(serializers.ModelSerializer):
    modelo = ModeloSerializerListar()
    class Meta:
        model = Pedido
        fields = '__all__'