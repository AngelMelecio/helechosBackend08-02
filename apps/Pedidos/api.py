from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Pedidos.models import Pedido
from apps.Produccion.models import Produccion
from apps.Pedidos.serializers import PedidoSerializer, PedidoSerializerListar, PedidoSerializerGetOne
from apps.DetallePedido.serializers import DetallePedidoSerializer
from apps.Produccion.serializers import ProduccionSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def pedido_api_view(request):
    # list
    if request.method == 'GET':
        pedidos = Pedido.objects.all().order_by('-fechaRegistro')
        print(pedidos)
        '''
        for pedido in Pedido.objects.all():
            total_empacado = 0
            total_ordinario = 0

            # Filtra los registros de producción de tipo 'Ordinario' para este pedido
            producciones_ordinarias = Produccion.objects.filter(detallePedido__pedido=pedido, tipo='Ordinario')
            total_ordinario = sum(produccion.cantidad for produccion in producciones_ordinarias)

            # Filtra los registros de producción 'Empacados' para este pedido
            producciones_empacadas = Produccion.objects.filter(detallePedido__pedido=pedido, estacionActual='empacado', tipo='Ordinario')
            total_empacado = sum(produccion.cantidad for produccion in producciones_empacadas)
           
            # Actualiza el pedido con el nuevo valor de 'progreso'
            pedido.paresTotales = total_ordinario
            pedido.paresProgreso = total_empacado
            pedido.estado = 'Terminado' if total_ordinario == total_empacado else 'Pendiente'
            pedido.save()
        '''
        pedido_serializer = PedidoSerializerListar(pedidos, many=True)
        return Response(pedido_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':

        # Separación pedido / detalles
        pedido = request.data.copy()
        detalles = pedido.get('detalles')
        pedido.pop('detalles')

        # Guardar el estado actual de la transacción
        sid = transaction.savepoint()
        success = True
        errors = []

        pedido_serializer = PedidoSerializer(data=pedido)
        if pedido_serializer.is_valid():

            # Guardar el pedido y obtener el nuevo id
            pedido_serializer.save()
            newPedidoId = pedido_serializer.data.get('idPedido')
            numEtiqueta = 1

            total=0

            for detalle in detalles:
                detalle['pedido'] = newPedidoId
                detallePedido_serializer = DetallePedidoSerializer(
                    data=detalle)
                if detallePedido_serializer.is_valid():

                    # Guardar el detalle del pedido y obtener el nuevo id
                    detallePedido_serializer.save()
                    newDetalleId = detallePedido_serializer.data['idDetallePedido']

                    # Iterar sobre las cantidades de cada detalle
                    cantidades = detalle.get('cantidades')
                    for cantidad in cantidades:
                        paquetes = 0
                        ultimoPaquete = 0
                        if cantidad['paquete'] != 0 :
                            paquetes = cantidad['cantidad'] / cantidad['paquete']
                            ultimoPaquete = cantidad['cantidad'] % cantidad['paquete']
                        for i in range(0, int(paquetes)):
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": str(numEtiqueta),
                                "cantidad": cantidad['paquete'],
                                "estacionActual": "creada",
                                "tallaReal": cantidad['talla']
                            }
                            total += cantidad['paquete']
                            # Guardar la etiqueta
                            produccion_serializer = ProduccionSerializer(data=etiqueta)
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                                numEtiqueta += 1
                            else:
                                errors.append(
                                    'No se pudieron generar las etiquetas, error en la solicitud.')
                                success = False

                        # Guardar la última etiqueta
                        if ultimoPaquete > 0:
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": str(numEtiqueta),
                                "cantidad": ultimoPaquete,
                                "estacionActual": "creada",
                                "tallaReal": cantidad['talla']
                            }
                            total += ultimoPaquete
                            produccion_serializer = ProduccionSerializer(data=etiqueta)
                            
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                                numEtiqueta += 1

                            else:
                                errors.append(
                                    'No se pudo generar la última etiqueta, error en la solicitud.')
                                success = False

                        Pedido.objects.filter(idPedido=newPedidoId).update(paresTotales=total)

                else:
                    print(detallePedido_serializer.errors)
                    errors.append(
                        'No se pudo crear el detalle del pedido, error en la solicitud.')
                    success = False
        else:
            errors.append('No se pudo crear pedido, error en la solicitud.')
            success = False

        # print('ERRORES: ', errors)
        if success:
            transaction.savepoint_commit(sid)
            return Response({
                'message': '¡Pedido creado correctamente!',
                'pedido': pedido_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            transaction.savepoint_rollback(sid)
            return Response({
                "message": 'Error al crear pedido',
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['GET', 'PATCH', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def pedido_detail_api_view(request, pk=None):
    pedido = Pedido.objects.filter(idPedido=pk).first()
    if pedido:
        # queryset
        if request.method == 'GET':
            # Obtener el pedido con detalles serializados
            pedido_serializer = PedidoSerializerGetOne(pedido)
            detalles = pedido_serializer.data.get('detalles')

            for detalle in detalles:
                idDetalle = detalle.get('idDetallePedido')
                cantidades = detalle.get('cantidades')
                for cantidad in cantidades:
                    
                    # Obtener las etiquetas de cada talla
                    etiquetas_estacion = Produccion.objects \
                        .filter(detallePedido__idDetallePedido=idDetalle, tallaReal=cantidad['talla'])
                    
                    etiquetas_estacion_serializer = ProduccionSerializer(etiquetas_estacion, many=True)
                    cantidad['etiquetas'] = etiquetas_estacion_serializer.data

            return Response(pedido_serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':  # Manejo de PATCH
            serializer = PedidoSerializer(pedido, data=request.data, partial=True)  # partial=True para actualización parcial
            if serializer.is_valid():
                serializer.save()
                return Response({'message': '¡Pedido Terminado!'}, status=status.HTTP_200_OK)
            return Response({'message': 'No fue posible cambiar el estado del pedido'}, status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'DELETE':
            pedido.delete()
            return Response({'message': 'Pedido eliminado correctamente'}, status=status.HTTP_200_OK)
    return Response(
        {'message':'No se encontró el pedido'}, 
        status=status.HTTP_400_BAD_REQUEST
    )