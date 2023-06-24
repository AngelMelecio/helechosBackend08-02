from rest_framework import serializers
from apps.Pedidos.models import Pedido
from apps.Modelos.serializers import ModeloSerializerListar,ModeloSerializerGetPedido
from apps.DetallePedido.serializers import DetallePedidoSerializerGetPedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoSerializerListar(serializers.ModelSerializer):
    modelo = ModeloSerializerListar()
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoSerializerGetOne(serializers.ModelSerializer):
    modelo = ModeloSerializerGetPedido()
    detalles = DetallePedidoSerializerGetPedido( source='detallepedido_set', many=True, read_only=True )
    class Meta:
        model = Pedido
        fields = '__all__'