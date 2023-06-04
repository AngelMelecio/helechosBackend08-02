from rest_framework import serializers
from apps.DetallePedido.models import DetallePedido
from apps.Pedidos.serializers import PedidoSerializerListar, PedidoSerializer
from apps.FichasTecnicas.serializers import FichaTecnicaSerializerListar, FichaTecnicaSerializerSimple

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model =DetallePedido
        fields = '__all__'

class DetallePedidoSerializerListar(serializers.ModelSerializer):
    pedido = PedidoSerializerListar()
    fichaTecnica = FichaTecnicaSerializerSimple()
    class Meta:
        model =DetallePedido
        fields = '__all__'