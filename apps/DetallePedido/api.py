from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.DetallePedido.models import DetallePedido
from apps.Produccion.models import Produccion
from apps.DetallePedido.serializers import DetallePedidoSerializer, DetallePedidoSerializerListar
from apps.Produccion.serializers import ProduccionSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def detallePedido_api_view(request):
    # list
    if request.method == 'GET':
        detallePedido = DetallePedido.objects.all()
        detallePedido_serializer = DetallePedidoSerializerListar(detallePedido,many=True)
        return Response( detallePedido_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        
        sid = transaction.savepoint()
        success = True

        detallePedido_serializer = DetallePedidoSerializer(data=request.data)
        if detallePedido_serializer.is_valid():
            detallePedido_serializer.save()

            # Crear etiquetas despus de guardar el detalle de pedido        
            newId = detallePedido_serializer.data['idDetallePedido']
            cantidades = request.data['cantidades']
            for cantidad in cantidades:
                paquetes = cantidad['cantidad'] / cantidad['paquete']
                ultimoPaquete = cantidad['cantidad'] % cantidad['paquete']

                for i in range(0, int(paquetes)):
                    etiqueta = {
                        "detallePedido": newId,
                        "numEtiqueta": i+1,
                        "cantidad": cantidad['paquete'],
                        "estacionActual": {"tejido":"corte"},
                        "tejido":"0",
                        "plancha":"-1",
                        "corte":"0",
                        "calidad":"0",
                        "empaque":"0",
                        "entrega":"0"
                    }
                    produccion_serializer = ProduccionSerializer(data=etiqueta)
                    if produccion_serializer.is_valid():
                        produccion_serializer.save()
                    else:
                        success = False

                if ultimoPaquete > 0:
                    etiqueta = {
                        "detallePedido": newId,
                        "numEtiqueta": int(paquetes)+1,
                        "cantidad": ultimoPaquete,
                        "estacionActual": {"tejido":"corte"},
                        "tejido":"0",
                        "plancha":"-1",
                        "corte":"0",
                        "calidad":"0",
                        "empaque":"0",
                        "entrega":"0"
                    }
                    produccion_serializer = ProduccionSerializer(data=etiqueta)
                    if produccion_serializer.is_valid():
                        produccion_serializer.save()
                    else:
                        success = False

            """
            detallesPedido = DetallePedido.objects.all()
            detallePedido_serializer = DetallePedidoSerializerListar(detallesPedido,many=True)
            return Response( {
                'message':'Detalle de pedido asignado correctamente!',
                'detallesPedido': detallePedido_serializer.data
            }, status=status.HTTP_201_CREATED )
            """

        
        else:
            success = False
            
        if success:
            transaction.savepoint_commit(sid)
            return Response( detallePedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        else:
            transaction.savepoint_rollback(sid)
            return Response( detallePedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def detallePedido_detail_api_view(request, pk=None):
    # Queryset
    detallePedido = DetallePedido.objects.filter( idDetallePedido = pk ).first()
    
    # Validacion
    if detallePedido:
        # Retrieve
        if request.method == 'GET':
            detallePedido_serializer =  DetallePedidoSerializerListar(detallePedido)
            return Response( detallePedido_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            detallePedido_serializer = DetallePedidoSerializer(detallePedido, data = request.data)
            if detallePedido_serializer.is_valid():
                detallePedido_serializer.save()
                detallesPedido = DetallePedido.objects.all()
                detallePedido_serializer = DetallePedidoSerializerListar(detallesPedido,many=True)
                return Response( {
                    'message':'¡Detalle de pedido actualizado correctamente!',
                    'detallesPedido': detallePedido_serializer.data
                }, status=status.HTTP_200_OK )
            print('ERROR', detallePedido_serializer.errors)
            return Response(detallePedido_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            detallePedido = DetallePedido.objects.filter( idDetallePedido = pk ).first()
            detallePedido.delete()
            return Response(
                {'message':'¡Detalle de pedido eliminado correctamente!'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el detalle de pedido'}, 
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def detallePedido_by_idPedido(request, pk=None):
    # Queryset
    detallesPedido = DetallePedido.objects.filter( pedido__idPedido = pk )
    
    if request.method == 'GET':
        detallePedido_serializer =  DetallePedidoSerializerListar(detallesPedido,many=True)
        for detalle in detallePedido_serializer.data:
            idDePe = detalle['idDetallePedido']
            arregloCantidades = detalle['cantidades']
            estadoDeProduccion=[]
            j=0
            for infoTalla in arregloCantidades:
                talla=infoTalla['talla']
                aux=['tejido','plancha','corte','calidad','empacado']
                i=0
                production=[]
                for dpto in aux:
                    production.insert(i,[dpto,Produccion.objects.filter(detallePedido__idDetallePedido=idDePe,tallaReal=talla,estacionActual=dpto).count()])
                    i=i+1
                objToInsert={"tittle":"Progreso de etiquetas talla "+talla,"data":production}
                estadoDeProduccion.insert(j,objToInsert)
            detalle['progreso']=estadoDeProduccion     
    return Response( detallePedido_serializer.data, status=status.HTTP_200_OK )   
   