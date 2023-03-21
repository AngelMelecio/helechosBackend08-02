from rest_framework import serializers
 
# import the todo data model
from apps.Modelos.models import Modelo
 
# create a serializer class
class ModeloSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Modelo
        fields = '__all__'