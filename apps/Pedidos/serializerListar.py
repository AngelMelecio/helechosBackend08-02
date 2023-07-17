from rest_framework import serializers
from apps.Pedidos.models import Pedido
from apps.Modelos.serializers import ModeloSerializerGetProduccion

class PedidoSerializerListar(serializers.ModelSerializer):
    modelo = ModeloSerializerGetProduccion()
    class Meta:
        model = Pedido
        fields = ('idPedido','modelo')