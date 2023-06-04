from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Pedidos.models import Pedido
from apps.Pedidos.serializers import PedidoSerializer, PedidoSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def pedido_api_view(request):
    # list
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedido_serializer = PedidoSerializerListar(pedidos,many=True)
        return Response( pedido_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        pedido_serializer = PedidoSerializer(data=request.data)
        if pedido_serializer.is_valid():
            pedido_serializer.save()
            pedidos = Pedido.objects.all()
            pedido_serializer = PedidoSerializerListar(pedidos,many=True)
            return Response( {
                'message':'¡Pedido creado correctamente!',
                'pedidos': pedido_serializer.data
            }, status=status.HTTP_201_CREATED )
        return Response( pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

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
 