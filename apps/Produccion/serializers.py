from rest_framework import serializers
from apps.Produccion.models import Produccion
from apps.Empleados.serializers import EmpleadoSerializer
from apps.Maquinas.serializers import MaquinaSerializer
from apps.DetallePedido.serializers import DetallePedidoSerializerGetPedido,DetallePedidoSerializerGetProduccion, DetallePedidoSerializerPostRegistro

class ProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produccion
        fields = '__all__'

class ProduccionSerializerListar(serializers.ModelSerializer):
    #General
    detallePedido = DetallePedidoSerializerGetProduccion()
    class Meta:
        model = Produccion
        fields = '__all__'

class ProduccionSerializerPostRegistro( serializers.ModelSerializer):
    detallePedido = DetallePedidoSerializerPostRegistro()
    class Meta:
        model = Produccion
        fields = ('idProduccion','detallePedido','estacionActual','numEtiqueta','tallaReal')
        