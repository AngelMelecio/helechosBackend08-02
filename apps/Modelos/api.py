from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Modelos.models import Modelo
from apps.Modelos.serializers import ModeloSerializer
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def modelo_api_view(request):
    # list
    if request.method == 'GET':
        modelos = Modelo.objects.all()
        modelo_serializer = ModeloSerializer(modelos,many=True)
        return Response( modelo_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        modelo_serializer = ModeloSerializer(data=request.data)
        if modelo_serializer.is_valid():
            modelo_serializer.save()
            return Response( {
                'message':'Modelo creado correctamente!.',
                'modelo': modelo_serializer.data
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
            modelo_serializer =  ModeloSerializer(modelo)
            return Response( modelo_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            modelo_serializer = ModeloSerializer(modelo, data = request.data)
            print( 'PUTTING' )
            print( request.data )
            if modelo_serializer.is_valid():
                modelo_serializer.save()
                return Response( {'message':'Modelo actualizado correctamente!.'}, status=status.HTTP_200_OK)
            return Response(modelo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            modelo = Modelo.objects.filter( idModelo = pk ).first()
            modelo.delete()
            return Response(
                {'message':'Modelo eliminado correctamente!.'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el modelo...'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 