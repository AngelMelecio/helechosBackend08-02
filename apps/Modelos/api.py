from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Modelos.models import Modelo
from apps.Modelos.serializers import ModeloSerializer, ModeloSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def modelo_api_view(request):
    # list
    if request.method == 'GET':
        modelos = Modelo.objects.all()
        modelo_serializer = ModeloSerializerListar(modelos,many=True)
        return Response( modelo_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        modelo_serializer = ModeloSerializer(data=request.data)
        if modelo_serializer.is_valid():
            modelo_serializer.save()
            modelos = Modelo.objects.all()
            modelo_serializer = ModeloSerializerListar(modelos,many=True)
            return Response( {
                'message':'¡Modelo creado correctamente!',
                'modelos': modelo_serializer.data
            }, status=status.HTTP_201_CREATED )
        return Response( modelo_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def modelo_detail_api_view(request, pk=None):
    # Queryset
    modelo = Modelo.objects.filter( idModelo = pk ).first()
    
    # Validacion
    if modelo:
        # Retrieve
        if request.method == 'GET':
            modelo_serializer =  ModeloSerializerListar(modelo)
            return Response( modelo_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            modelo_serializer = ModeloSerializer(modelo, data = request.data)
            if modelo_serializer.is_valid():
                modelo_serializer.save()
                modelos = Modelo.objects.all()
                modelo_serializer = ModeloSerializerListar(modelos,many=True)
                return Response( {
                    'message':'¡Modelo actualizado correctamente!',
                    'modelos': modelo_serializer.data
                }, status=status.HTTP_200_OK )
            print('ERROR', modelo_serializer.errors)
            return Response(modelo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            modelo = Modelo.objects.filter( idModelo = pk ).first()
            modelo.delete()
            return Response(
                {'message':'¡Modelo eliminado correctamente!'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el modelo'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 
@api_view(['GET'])
@parser_classes([MultiPartParser , JSONParser])
def modelos_cliente_api_view(request, pk=None):
    modelos = Modelo.objects.filter( cliente__idCliente = pk )
    if modelos:
        if request.method == 'GET':
            modelo_serializer = ModeloSerializerListar(modelos,many=True)
            return Response( modelo_serializer.data, status=status.HTTP_200_OK )
    
    return Response( [] , status=status.HTTP_200_OK )
