from rest_framework import serializers
 
from apps.FichasTecnicas.models import FichaTecnica
from apps.Modelos.serializers import ModeloSerializerListar,ModeloSerializerGetProduccion
from apps.Maquinas.serializers import MaquinaSerializer
from apps.FichaTecnicaMaterial.serializers import FichaMaterialesSerializerGetPedido
from apps.Materiales.serializers import MaterialSerializerGetPedido

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
class FichaTecnicaSerializerExtraCorto(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = ('idFichaTecnica','nombre','talla','fotografia')


class FichaTecnicaSerializerGetPedido(serializers.ModelSerializer):
    
    materiales = serializers.SerializerMethodField()
    
    class Meta:
        model = FichaTecnica
        fields = ('idFichaTecnica','nombre','fotografia','talla','materiales','fechaCreacion','fechaUltimaEdicion')

    def get_materiales(self, obj):
        fichas_materiales = obj.fichatecnicamaterial_set.filter(material__tipo='Poliester')
        serializer = FichaMaterialesSerializerGetPedido(fichas_materiales, many=True)
        fichas = serializer.data
        materiales =  []
        for ficha in fichas:
            materiales.append( ficha['material'] )
        return materiales
    
class FichaTecnicaSerializerGetProduccion(serializers.ModelSerializer):
    
    materiales = serializers.SerializerMethodField()
    modelo = ModeloSerializerGetProduccion()
    
    class Meta:
        model = FichaTecnica
        fields = ('idFichaTecnica','materiales','modelo')

    def get_materiales(self, obj):
        fichas_materiales = obj.fichatecnicamaterial_set.filter(material__tipo='Poliester')
        serializer = FichaMaterialesSerializerGetPedido(fichas_materiales, many=True)
        fichas = serializer.data
        materiales =  []
        for ficha in fichas:
            materiales.append( ficha['material'] )
        return materiales