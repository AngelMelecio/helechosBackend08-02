from rest_framework import serializers
 
# import the todo data model
from apps.Maquinas.models import Maquina
 
# create a serializer class
class MaquinaSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Maquina
        fields = '__all__'