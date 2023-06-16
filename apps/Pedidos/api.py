from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Pedidos.models import Pedido
from apps.Produccion.models import Produccion
from apps.Pedidos.serializers import PedidoSerializer, PedidoSerializerListar
from apps.DetallePedido.serializers import DetallePedidoSerializer
from apps.Produccion.serializers import ProduccionSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def pedido_api_view(request):
    # list
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedido_serializer = PedidoSerializerListar(pedidos,many=True)
        for pedido in pedido_serializer.data:
            id=pedido.get('idPedido')
            ready = Produccion.objects.filter(detallePedido__pedido__idPedido=id, estacionActual='empacado').count()
            goal = Produccion.objects.filter(detallePedido__pedido__idPedido=id).count()
            progress=int((ready*100)/goal)
            color_ranges = [
                (0, 25, '#9b1b1b'),
                (26, 50, '#ea580c'),
                (51, 75, '#eab308'),
                (76, 100, '#15803d'),
            ]
            color = '#ffffff'
            for lower_bound, upper_bound, associated_color in color_ranges:
                if lower_bound <= progress <= upper_bound:
                    color = associated_color
                    break
            pedido['progressBar'] = {"progress":progress,"goal":100,"color":color}
        return Response( pedido_serializer.data, status=status.HTTP_200_OK )
    # Create
    elif request.method == 'POST':
    
        # Separar el pedido de los detalles
        pedido = request.data.copy()
        detalles = pedido.get('detalles')
        pedido.pop('detalles')
        
        

        # Guardar el estado actual
        sid = transaction.savepoint()
        success = True
        errors = []

        pedido_serializer = PedidoSerializer(data=pedido)
        
        if pedido_serializer.is_valid(): 
            pedido_serializer.save()
            newPedidoId = pedido_serializer.data.get('idPedido')
            
            for detalle in detalles:
                detalle['pedido'] = newPedidoId
                detallePedido_serializer = DetallePedidoSerializer(data=detalle)
                if detallePedido_serializer.is_valid():
                    detallePedido_serializer.save()
                    newDetalleId = detallePedido_serializer.data['idDetallePedido']
                    cantidades = detalle.get('cantidades')

                    for cantidad in cantidades:
                        paquetes = cantidad['cantidad'] / cantidad['paquete']
                        ultimoPaquete = cantidad['cantidad'] % cantidad['paquete']
                        
                        for i in range(0, int(paquetes)):
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": i+1,
                                "cantidad": cantidad['paquete'],
                                "estacionActual":"creada",
                                "tallaReal":cantidad['talla']
                                
                            }
                            produccion_serializer = ProduccionSerializer(data=etiqueta)
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                            else:
                                errors.append('No se pudieron generar las etiquetas, error en la solicitud.')
                                success = False

                        if ultimoPaquete > 0:
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": int(paquetes)+1,
                                "cantidad": ultimoPaquete,
                                "estacionActual":"creada",
                                "tallaReal":cantidad['talla']
                            }
                            produccion_serializer = ProduccionSerializer(data=etiqueta)
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                            else:
                                errors.append('No se pudo crear pedido 1, error en la solicitud.')
                                success = False
                else:
                    print(detallePedido_serializer.errors)
                    errors.append('No se pudo crear pedido 2, error en la solicitud.')
                    success = False
        else:
            # append new error in errors array
            errors.append('No se pudo crear pedido 3, error en la solicitud.')
            success = False

        print('ERRORES: ', errors)
        if success :
            transaction.savepoint_commit(sid)
            return Response( {
                'message':'¡Pedido creado correctamente!',
                'pedido': pedido_serializer.data
            }, status=status.HTTP_201_CREATED )
        else:
            transaction.savepoint_rollback(sid)
            return Response( {
                "message": 'Error al crear pedido',
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST )
    

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def pedido_detail_api_view(request, pk=None):
    # Queryset
    pedido = Pedido.objects.filter( idPedido = pk ).first()
    
    # Validacion
    if pedido:
        # Retrieve
        if request.method == 'GET':
            pedido_serializer =  PedidoSerializerListar(pedido)
            return Response( pedido_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            pedido_serializer = PedidoSerializer(pedido, data = request.data)
            if pedido_serializer.is_valid():
                pedido_serializer.save()
                pedidos = Pedido.objects.all()
                pedido_serializer =PedidoSerializerListar(pedidos,many=True)
                return Response( {
                    'message':'¡Pedido actualizado correctamente!',
                    'pedidos': pedido_serializer.data
                }, status=status.HTTP_200_OK )
            print('ERROR', pedido_serializer.errors)
            return Response(pedido_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            pedido = Pedido.objects.filter( idPedido = pk ).first()
            pedido.delete()
            return Response(
                {'message':'¡Pedido eliminado correctamente!'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el pedido'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 