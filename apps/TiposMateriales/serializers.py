from rest_framework import serializers
 
from apps.TiposMateriales.models import TipoMaterial
 

class TiposMaterialesSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = TipoMaterial
        fields = '__all__'