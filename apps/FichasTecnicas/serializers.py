from rest_framework import serializers
 
from apps.FichasTecnicas.models import FichaTecnica
from apps.Modelos.serializers import ModeloSerializerListar
from apps.Maquinas.serializers import MaquinaSerializer

class FichaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = '__all__'

class FichaTecnicaSerializerListar(serializers.ModelSerializer):
    modelo = ModeloSerializerListar()
    maquinaTejido = MaquinaSerializer() 
    maquinaPlancha = MaquinaSerializer()
    class Meta:
        model = FichaTecnica
        fields = '__all__'

class FichaTecnicaSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = ('idFichaTecnica','nombre','fotografia','talla','fechaCreacion','fechaUltimaEdicion')