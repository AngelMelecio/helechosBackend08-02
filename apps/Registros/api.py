from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Registros.models import Registro
from apps.Registros.serializers import RegistroSerializer, RegistroSerializerListar
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.parsers import JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def registro_api_view(request):
    # list
    if request.method == 'GET':
        registros = Registro.objects.all()
        registro_serializer = RegistroSerializerListar(registros,many=True)
        return Response( registro_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        registro_serializer = RegistroSerializer(data=request.data)
        if registro_serializer.is_valid():
            registro_serializer.save()
            return Response( {'message':'¡Registro creado correctamente!'}, status=status.HTTP_201_CREATED )
        return Response( registro_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def registro_detail_api_view(request, pk=None ):
    # Queryset
    registro = Registro.objects.filter( idRegistro = pk ).first()
    
    # Validacion
    if registro:
        # Retrieve
        if request.method == 'GET':
            registro_serializer =  RegistroSerializer(registro)
            return Response( registro_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            registro_serializer = RegistroSerializer(registro, data = request.data)
            print( 'PUTTING' )

            if registro_serializer.is_valid():
                registro_serializer.save()
                return Response( {'message':'¡Registro actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response(registro_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            registro = Registro.objects.filter( idRegistro = pk ).first()
            registro.delete()
            return Response(
                {'message':'¡Registro eliminado correctamente!'}, 
                status=status.HTTP_200_OK
            )
   
    return Response(
        {'message':'No se encontró el registro'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
        