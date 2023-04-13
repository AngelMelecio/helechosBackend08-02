from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.FichasTecnicas.models import FichaTecnica
from apps.FichasTecnicas.serializers import FichaTecnicaSerializer, FichaTecnicaSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def ficha_tecnica_api_view(request):
    # list
    if request.method == 'GET':
        fichas = FichaTecnica.objects.all()
        ficha_serializer = FichaTecnicaSerializerListar(fichas,many=True)
        return Response( ficha_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        ficha_serializer = FichaTecnicaSerializer(data=request.data)
        if ficha_serializer.is_valid():
            ficha_serializer.save()
            return Response( {
                'message':'Ficha técnica creada correctamente!',
                'ficha': ficha_serializer.data
            }, status=status.HTTP_201_CREATED )
        return Response( ficha_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def ficha_tecnica_detail_api_view(request, pk=None):
    # Queryset
    ficha = FichaTecnica.objects.filter( idFichaTecnica = pk ).first()
    
    # Validacion
    if ficha:
        # Retrieve
        if request.method == 'GET':
            ficha_serializer =  FichaTecnicaSerializer(ficha)
            return Response( ficha_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            ficha_serializer = FichaTecnicaSerializer(ficha, data = request.data)
            if ficha_serializer.is_valid():
                ficha_serializer.save()
                return Response( {'message':'Ficha técnica actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response(ficha_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            ficha = FichaTecnica.objects.filter( idFichaTecnica = pk ).first()
            ficha.delete()
            return Response(
                {'message':'Ficha técnica eliminada correctamente!'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró la ficha técnica'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 