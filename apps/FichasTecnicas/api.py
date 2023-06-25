from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.FichasTecnicas.models import FichaTecnica
from apps.FichaTecnicaMaterial.models import FichaTecnicaMaterial

from apps.FichasTecnicas.serializers \
    import FichaTecnicaSerializer, \
    FichaTecnicaSerializerListar,\
    FichaTecnicaSerializerSimple, \
    FichaTecnicaSerializerGetPedido

from apps.FichaTecnicaMaterial.serializers import FichaTecnicaMaterialSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser
# crear una api para listar las fichas tecnicas en base al modelo


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def ficha_tecnica_api_view(request):
    # list
    if request.method == 'GET':
        fichas = FichaTecnica.objects.all()
        ficha_serializer = FichaTecnicaSerializerListar(fichas, many=True)
        return Response(ficha_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':
        ficha_serializer = FichaTecnicaSerializer(data=request.data)
        if ficha_serializer.is_valid():
            ficha_serializer.save()
            idModelo = request.data.get('modelo')
            fichas = FichaTecnica.objects.filter(modelo_id=idModelo)
            fichas_serializer = FichaTecnicaSerializerListar(fichas, many=True)
            return Response({
                'fichas': fichas_serializer.data,
                'message': 'Ficha técnica creada correctamente!',
                'ficha': ficha_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(ficha_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def ficha_tecnica_detail_api_view(request, pk=None):
    # Queryset
    fichas = FichaTecnica.objects.filter(modelo_id=pk)

    # Retrieve
    if request.method == 'GET':
        ficha_serializer = FichaTecnicaSerializerListar(fichas, many=True)
        return Response(ficha_serializer.data, status=status.HTTP_200_OK)

    # Update
    elif request.method == 'PUT':
        ficha = FichaTecnica.objects.filter(idFichaTecnica=pk).first()
        ficha_serializer = FichaTecnicaSerializer(ficha, data=request.data)
        if ficha_serializer.is_valid():
            ficha_serializer.save()
            idModelo = request.data.get('modelo')
            fichas = FichaTecnica.objects.filter(modelo_id=idModelo)
            fichas_serializer = FichaTecnicaSerializerListar(fichas, many=True)
            return Response({
                'fichas': fichas_serializer.data,
                'ficha': ficha_serializer.data,
                'message': 'Ficha técnica actualizada correctamente!'
            }, status=status.HTTP_200_OK)
        else:
            print("ERRORES")
            print(ficha_serializer.errors)
        return Response(ficha_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ficha = FichaTecnica.objects.filter(idFichaTecnica=pk).first()
        ficha.delete()
        return Response(
            {'message': 'Ficha técnica eliminada correctamente!'},
            status=status.HTTP_200_OK
        )

    return Response(
        {'message': 'No se encontró la ficha técnica'},
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def fichas_tecnicas_with_materials_view(request, pk=None):
    # Queryset
    fichas = FichaTecnica.objects.filter(modelo_id=pk)

    # Retrieve
    if request.method == 'GET':
        ficha_serializer = FichaTecnicaSerializerSimple(fichas, many=True)
        fichas=ficha_serializer.data  

        for ficha in fichas:
            id=ficha['idFichaTecnica']
            materiales=FichaTecnicaMaterial.objects.filter(fichaTecnica=id , material__tipo='Poliester')
            materiales_serializer = FichaTecnicaMaterialSerializerListar(materiales,many=True)
            ficha['materiales']=materiales_serializer.data

        return Response(ficha_serializer.data, status=status.HTTP_200_OK)

    

    return Response(
        {'message': 'No se encontró la ficha técnica'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def fichas_by_modelo(request, pk=None): 
    fichas = FichaTecnica.objects.filter(modelo_id=pk)
    # Retrieve
    if request.method == 'GET':
        ficha_serializer = FichaTecnicaSerializerGetPedido(fichas, many=True)
        return Response(ficha_serializer.data, status=status.HTTP_200_OK)