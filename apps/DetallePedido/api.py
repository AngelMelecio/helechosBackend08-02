from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.DetallePedido.models import DetallePedido
from apps.DetallePedido.serializers import DetallePedidoSerializer, DetallePedidoSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

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
        detallePedido_serializer = DetallePedidoSerializer(data=request.data)
        if detallePedido_serializer.is_valid():
            detallePedido_serializer.save()
            detallesPedido = DetallePedido.objects.all()
            detallePedido_serializer = DetallePedidoSerializerListar(detallesPedido,many=True)
            return Response( {
                'message':'Detalle de pedido asignado correctamente!',
                'detallesPedido': detallePedido_serializer.data
            }, status=status.HTTP_201_CREATED )
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
 