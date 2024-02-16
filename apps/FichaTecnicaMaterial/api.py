from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.DetallePedido.models import DetallePedido
from apps.FichasTecnicas.models import FichaTecnica
from apps.Produccion.models import Produccion
from django.db.models import Sum
from apps.FichasTecnicas.serializers import FichaTecnicaSerializerExtraCorto
from apps.FichaTecnicaMaterial.models import FichaTecnicaMaterial
from apps.FichaTecnicaMaterial.serializers import FichaTecnicaMaterialSerializer
from apps.FichaTecnicaMaterial.serializers import FichaTecnicaMaterialSerializerListar,FichaTecnicaMaterialSerializerListarCorto
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['POST'])
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
def materiales_by_fichaTecnica(request, pkFichaTecnica):
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

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def materiales_by_pedido(request, pkPedido):
    detallesPedido=DetallePedido.objects.filter(pedido=pkPedido)
    toResponse=[]
    for detalle in detallesPedido:
        fichaTecnicaMaterial = FichaTecnicaMaterial.objects.filter(fichaTecnica=detalle.fichaTecnica)
        materiales = FichaTecnicaMaterialSerializerListarCorto(fichaTecnicaMaterial, many=True)

        fichaTecnica = FichaTecnica.objects.filter(idFichaTecnica=detalle.fichaTecnica.idFichaTecnica).first()
        fichaTecnicaSerializer = FichaTecnicaSerializerExtraCorto(fichaTecnica)

        fichaTecnica = fichaTecnicaSerializer.data
        fichaTecnica['materiales'] = materiales.data
        print(detalle.idDetallePedido)
        # Suponiendo que 'detalle.idDetallePedido' es el ID que quieres filtrar
        paresOrdinarios = Produccion.objects.filter(detallePedido=detalle.idDetallePedido, tipo='Ordinario').aggregate(total_cantidad=Sum('cantidad'))
        # 'paresOrdinarios' es ahora un diccionario que contiene el total sumado bajo la clave 'total_cantidad'
        total_cantidad_ordinarios = paresOrdinarios['total_cantidad']
        # Si no hay objetos que coincidan con el filtro, 'total_cantidad' será None
        if total_cantidad_ordinarios is None:
            total_cantidad_ordinarios = 0

        paresReposicion = Produccion.objects.filter(detallePedido=detalle.idDetallePedido, tipo='Reposicion').aggregate(total_cantidad=Sum('cantidad'))
        total_cantidad_reposicion = paresReposicion['total_cantidad']
        if total_cantidad_reposicion is None:
            total_cantidad_reposicion = 0

        paresExtra = Produccion.objects.filter(detallePedido=detalle.idDetallePedido, tipo='Extra').aggregate(total_cantidad=Sum('cantidad'))
        total_cantidad_extra = paresExtra['total_cantidad']
        if total_cantidad_extra is None:
            total_cantidad_extra = 0
        
        toResponse.append({
            'idDetallePedido':detalle.idDetallePedido,
            'fichaTecnica':fichaTecnica,
            'cantidades':{
                'ordinario':total_cantidad_ordinarios,
                'reposicion':total_cantidad_reposicion,
                'extra':total_cantidad_extra
            }
        })
  
    return Response( toResponse, status=status.HTTP_200_OK )
