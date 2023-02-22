from rest_framework import serializers,viewsets
 
# import the todo data model
from apps.Empleados.models import Empleado
 



# create a serializer class
class EmpleadoSerializer(serializers.ModelSerializer):
 
    image_url = serializers.ImageField(required=False, use_url=True)

    # create a meta class
    class Meta:
        model = Empleado
        fields = '__all__'
"""
    def get_photo_url(self, obj):
        request = self.context.get('request')
        fotografia = obj.fingerprint.url
        return request.build_absolute_uri(fotografia)
"""