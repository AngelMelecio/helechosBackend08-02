from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Maquinas.models import Maquina
from apps.Maquinas.serializers import MaquinaSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def maquina_api_view(request):
    # list
    if request.method == 'GET':
        maquinas = Maquina.objects.all()
        maquinas_serializer = MaquinaSerializer(maquinas,many=True)
        return Response( maquinas_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        maquina_serializer = MaquinaSerializer(data=request.data)
        if maquina_serializer.is_valid():
            maquina_serializer.save()
            return Response( {'message':'¡Máquina creada correctamente!'}, status=status.HTTP_201_CREATED )
        return Response( maquina_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def maquina_detail_api_view(request, pk=None ):
    # Queryset
    maquina = Maquina.objects.filter( idMaquina = pk ).first()
    
    # Validacion
    if maquina:
        # Retrieve
        if request.method == 'GET':
            maquina_serializer =  MaquinaSerializer(maquina)
            return Response( maquina_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            maquina_serializer = MaquinaSerializer(maquina, data = request.data)
            if maquina_serializer.is_valid():
                maquina_serializer.save()
                return Response( {'message':'¡Máquina actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response(maquina_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            maquina = Maquina.objects.filter( idMaquina = pk ).first()
            try:
                maquina.delete()
                return Response(
                    {'message':'¡Máquina eliminada correctamente!'}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message':'¡No es posible eliminar una máquina en uso!'}, 
                    status=status.HTTP_409_CONFLICT
                )

    return Response(
        {'message':'No se encontró la máquina'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
        