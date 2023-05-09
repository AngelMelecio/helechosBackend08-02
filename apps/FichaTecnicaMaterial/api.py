from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.FichaTecnicaMaterial.models import FichaTecnicaMaterial
from apps.FichaTecnicaMaterial.serializers import FichaTecnicaMaterialSerializer
from apps.FichaTecnicaMaterial.serializers import FichaTecnicaMaterialSerializerListar
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['POST','GET'])
@parser_classes([MultiPartParser, JSONParser])
def ficha_tecnica_material_post_api_view(request):
    #Post
    if request.method == 'POST':
        sid = transaction.savepoint() 

        idFichaTecnica = request.data.get('idFichaTecnica')
        materiales = request.data.get('materiales')
        success = True
        #revisar eficacia de estos metodos y cual puede ser mejor: (editar -insertar) o (eliminar - insertar)
        FichaTecnicaMaterial.objects.select_for_update().filter( fichaTecnica = idFichaTecnica ).delete()
        for m in materiales:
            objFichaTecnicaMaterial = { 'fichaTecnica':idFichaTecnica, 'material':m.get('idMaterial'), 'guiaHilos':m.get('guiaHilos'), 'hebras':int(m.get('hebras')), 'peso':float(m.get('peso'))}
            fichaTecnicaMaterial_serializer = FichaTecnicaMaterialSerializer( data=objFichaTecnicaMaterial )
            if fichaTecnicaMaterial_serializer.is_valid():
                fichaTecnicaMaterial_serializer.save()
            else:
                print('ERROR')
                print(fichaTecnicaMaterial_serializer.errors)
                success = False
        if success:
            transaction.savepoint_commit(sid)
            return Response({'message':'¡Asignación correcta de materiales!'}, status=status.HTTP_200_OK)
        else:
            transaction.savepoint_rollback(sid)
            return Response({'message':'Ha ocurrido un error durante la asignación de materiales'}, status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def ficha_tecnica_material_get_one_api_view(request, pkFichaTecnica):
    # Queryset
    fichaTecnicaMaterial = FichaTecnicaMaterial.objects.filter(fichaTecnica=pkFichaTecnica)
    # Validacion
    if fichaTecnicaMaterial:
        # Retrieve
        if request.method == 'GET':
            fichaTecnicaMaterialSerializerListar = FichaTecnicaMaterialSerializerListar(fichaTecnicaMaterial, many=True)
            return Response(
                {
                    'materiales':fichaTecnicaMaterialSerializerListar.data,
                    'message': 'Materiales relacionados encontrados'
                },
                status=status.HTTP_200_OK)
    return Response(
        { 
            'materiales':[],
            'message': 'No se encontraron materiales relacionados'
        },
        status=status.HTTP_200_OK
    )