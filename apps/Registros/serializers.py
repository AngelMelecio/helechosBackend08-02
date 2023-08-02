from rest_framework import serializers
from apps.Registros.models import Registro
from apps.Empleados.serializers import EmpleadoSerializerToRegistros
from apps.Maquinas.serializers import MaquinaSerializerToRegistros
from apps.Produccion.serializers import ProduccionSerializerListar

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = '__all__'

class RegistroSerializerListar(serializers.ModelSerializer):
    empleado = EmpleadoSerializerToRegistros()
    maquina = MaquinaSerializerToRegistros()
    produccion= ProduccionSerializerListar()
    class Meta:
        model = Registro
        fields = '__all__'

class RegistroSerializerToChart(serializers.ModelSerializer):
    empleado = EmpleadoSerializerToRegistros()
    maquina = MaquinaSerializerToRegistros()
    class Meta:
        model = Registro
        fields = '__all__'