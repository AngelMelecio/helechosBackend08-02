from rest_framework import serializers
from apps.DetallePedido.models import DetallePedido
from apps.FichasTecnicas.serializers import FichaTecnicaSerializerGetPedido,FichaTecnicaSerializerGetProduccion
from apps.Pedidos.serializerListar import PedidoSerializerListar

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model =DetallePedido
        fields = '__all__'

"""class DetallePedidoSerializerListar(serializers.ModelSerializer):
    pedido = PedidoSerializerListar()
    fichaTecnica = FichaTecnicaSerializerSimple()
    class Meta:
        model =DetallePedido
        fields = '__all__'
"""

class DetallePedidoSerializerListar(serializers.ModelSerializer):
    #pedido = PedidoSerializerListar()
    class Meta:
        model =DetallePedido
        fields = '__all__'

class DetallePedidoSerializerGetPedido(serializers.ModelSerializer):
    fichaTecnica=FichaTecnicaSerializerGetPedido()
    class Meta:
        model =DetallePedido
        fields = ('idDetallePedido','fichaTecnica','cantidades','rutaProduccion')

class DetallePedidoSerializerGetProduccion(serializers.ModelSerializer):
    fichaTecnica=FichaTecnicaSerializerGetProduccion()
    class Meta:
        model =DetallePedido
        fields = ('idDetallePedido','fichaTecnica','pedido','rutaProduccion')

class DetallePedidoSerializerPostRegistro(serializers.ModelSerializer):
    pedido=PedidoSerializerListar()
    class Meta:
        model = DetallePedido
        fields = ('idDetallePedido', 'rutaProduccion','pedido')