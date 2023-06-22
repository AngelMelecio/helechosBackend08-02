from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Pedidos.models import Pedido
from apps.Produccion.models import Produccion
from apps.DetallePedido.models import DetallePedido
from apps.Pedidos.serializers import PedidoSerializer, PedidoSerializerListar,PedidoSerializerGetOne
from apps.DetallePedido.serializers import DetallePedidoSerializer,DetallePedidoSerializerListar,DetallePedidoSerializerGetPedido
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
            ready = Produccion.objects.filter(detallePedido__pedido__idPedido=id, estacionActual='empacado'or'entregado').count()
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
                                errors.append('No se pudo generar la última etiqueta, error en la solicitud.')
                                success = False
                else:
                    print(detallePedido_serializer.errors)
                    errors.append('No se pudo crear el detalle del pedido, error en la solicitud.')
                    success = False
        else:
            # append new error in errors array
            errors.append('No se pudo crear pedido, error en la solicitud.')
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

    #detallesPedido = DetallePedido.objects.filter( pedido__idPedido = pk )
    
    if request.method == 'GET':
        objToResponse = {}
        pedido= Pedido.objects.filter( idPedido = pk ).first()
        pedido_serializer = PedidoSerializerGetOne(pedido)
        
        detallesPedido = DetallePedido.objects.filter( pedido__idPedido = pk )

        detallePedido_serializer =  DetallePedidoSerializerGetPedido(detallesPedido,many=True)
        for detalle in detallePedido_serializer.data:

            objDetalleToResponse = {}
            objDetalleToResponse['idFichaTecnica'] = detalle.get('fichaTecnica').get('idFichaTecnica')
            objDetalleToResponse['nombre'] = detalle.get('fichaTecnica').get('nombre')
            objDetalleToResponse['fotografia'] = detalle.get('fichaTecnica').get('fotografia')
            objDetalleToResponse['talla'] = detalle.get('fichaTecnica').get('talla')

            
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



        objToResponse['pedido'] = pedido_serializer.data.get('idPedido')
        objToResponse['modelo'] = pedido_serializer.data.get('modelo').get('idModelo')
        objToResponse['cliente'] = pedido_serializer.data.get('modelo').get('cliente')
        objToResponse['fechaRegistro'] = pedido_serializer.data.get('fechaRegistro')
        objToResponse['fechaEntrega'] = pedido_serializer.data.get('fechaEntrega')
        objToResponse['detalles'] =  objDetalleToResponse
        

      
    return Response(objToResponse, status=status.HTTP_200_OK ) 
    
    
   