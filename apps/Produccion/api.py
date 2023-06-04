from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Produccion.models import Produccion
from apps.Produccion.serializers import ProduccionSerializer, ProduccionSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def produccion_api_view(request):
    # list
    if request.method == 'GET':
        listaProduccion = Produccion.objects.all()
        produccion_serializer = ProduccionSerializerListar(listaProduccion,many=True)
        return Response( produccion_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        produccion_serializer = ProduccionSerializer(data=request.data)
        if produccion_serializer.is_valid():
            produccion_serializer.save()
            return Response( {
                'message':'¡Registro de producción creado correctamente!',
            }, status=status.HTTP_201_CREATED )
        return Response( produccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def produccion_detail_api_view(request, pk=None):
    # Queryset
    registroProduccion = Produccion.objects.filter( idProduccion = pk ).first()
    
    # Validacion
    if registroProduccion:
        # Retrieve
        if request.method == 'GET':
            produccion_serializer =  ProduccionSerializerListar(registroProduccion)
            return Response( produccion_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            produccion_serializer = ProduccionSerializer(registroProduccion, data = request.data)
            if produccion_serializer.is_valid():
                produccion_serializer.save()
               
                return Response( {
                    'message':'¡Registro de producción actualizado correctamente!'
                }, status=status.HTTP_200_OK )
            print('ERROR', produccion_serializer.errors)
            return Response(produccion_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            registroProduccion = Produccion.objects.filter( idProduccion = pk ).first()
            registroProduccion.delete()
            return Response(
                {'message':'¡Registro de producción eliminado correctamente!'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el registro de producción'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 