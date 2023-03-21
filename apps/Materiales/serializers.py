from rest_framework import serializers
 
# import the todo data model
from apps.Materiales.models import Material
 
# create a serializer class
class MaterialSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Material
        fields = '__all__'