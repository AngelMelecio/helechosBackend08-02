from rest_framework import serializers
from apps.Reposiciones.models import Reposicion
from apps.Empleados.serializers import EmpleadoSerializerToRegistros
from apps.Maquinas.serializers import MaquinaSerializerToRegistros

class ReposicionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Reposicion
        fields = '__all__'

class ReposicionSerilizerGet(serializers.ModelSerializer):
    empleadoFalla = EmpleadoSerializerToRegistros()
    empleadoReponedor = EmpleadoSerializerToRegistros()
    maquina = MaquinaSerializerToRegistros()
    class Meta:
        model = Reposicion
        fields = ('cantidad','motivos','empleadoFalla','empleadoReponedor','maquina','fecha')