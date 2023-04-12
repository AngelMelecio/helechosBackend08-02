from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.ModeloMaterial.models import ModeloMaterial
from apps.ModeloMaterial.serializers import ModeloMaterialSerializer
from apps.ModeloMaterial.serializers import ModeloMaterialSerializerListar
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['POST','GET'])
@parser_classes([MultiPartParser, JSONParser])
def modelo_material_post_api_view(request):
    #Post
    if request.method == 'POST':
        sid = transaction.savepoint()

        idModelo = request.data.get('idModelo')
        materiales = request.data.get('materiales')
        success = True

        ModeloMaterial.objects.select_for_update().filter( modelo = idModelo ).delete()
        for m in materiales:
            modelo_material = { 'modelo':idModelo, 'material':m.get('idMaterial'), 'guiaHilos':m.get('guiaHilos'), 'hebras':m.get('hebras'), 'peso':m.get('peso')}
            modeloMaterial_serializer = ModeloMaterialSerializer( data=modelo_material )
            if modeloMaterial_serializer.is_valid():
                modeloMaterial_serializer.save()
            else:
                success = False
        if success:
            transaction.savepoint_commit(sid)
            return Response({'message':'¡Asignación correcta de materiales!'}, status=status.HTTP_200_OK)
        else:
            transaction.savepoint_rollback(sid)
            return Response({'message':'Ha ocurrido un error durante la asignación de materiales'}, status=status.HTTP_409_CONFLICT)
    
     # list
    if request.method == 'GET':
        modeloMateriales = ModeloMaterial.objects.all()
        modeloMaterial_serializer = ModeloMaterialSerializerListar(modeloMateriales, many=True)
        return Response(modeloMaterial_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def modelo_material_get_one_api_view(request, pkModelo):
    # Queryset
    modeloMaterial = ModeloMaterial.objects.filter(modelo=pkModelo)
    # Validacion
    if modeloMaterial:
        # Retrieve
        if request.method == 'GET':
            modeloMaterialSerializerListar = ModeloMaterialSerializerListar(modeloMaterial, many=True)
            return Response(modeloMaterialSerializerListar.data, status=status.HTTP_200_OK)
    return Response(
        {'message': 'No se encontraron materiales relacionados'},
        status=status.HTTP_200_OK
    )