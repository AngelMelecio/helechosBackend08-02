from rest_framework import serializers
from apps.Produccion.models import Produccion
from apps.Empleados.serializers import EmpleadoSerializer
from apps.Maquinas.serializers import MaquinaSerializer
from apps.DetallePedido.serializers import DetallePedidoSerializerListar

class ProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produccion
        fields = '__all__'

class ProduccionSerializerListar(serializers.ModelSerializer):
    #General
    detallePedido = DetallePedidoSerializerListar()
    #Empleados
    tejedor = EmpleadoSerializer()
    planchador = EmpleadoSerializer()
    cortador = EmpleadoSerializer()
    inspector = EmpleadoSerializer()
    empacador = EmpleadoSerializer()
    repartidor = EmpleadoSerializer()
    #Maquinas
    maquinaTejidoProduccion=MaquinaSerializer()
    maquinaPlanchaProduccion=MaquinaSerializer()
    maquinaCorteProduccion=MaquinaSerializer()
    class Meta:
        model = Produccion
        fields = '__all__'