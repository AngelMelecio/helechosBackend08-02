from rest_framework import serializers
 
# import the todo data model
from apps.Clientes.models import Cliente
 

# create a serializer class
class ClienteSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Cliente
        fields = '__all__'
