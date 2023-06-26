from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Pedidos.models import Pedido
from apps.Produccion.models import Produccion
from apps.DetallePedido.models import DetallePedido
from apps.FichaTecnicaMaterial.models import FichaTecnicaMaterial
from apps.FichaTecnicaMaterial.serializers import FichaMaterialesSerializerGetPedido
from apps.Pedidos.serializers import PedidoSerializer, PedidoSerializerListar, PedidoSerializerGetOne
from apps.DetallePedido.serializers import DetallePedidoSerializer, DetallePedidoSerializerListar, DetallePedidoSerializerGetPedido
from apps.Produccion.serializers import ProduccionSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from django.db import transaction
from django.db.models import Sum, Count


@transaction.atomic
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def pedido_api_view(request):
    # list
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedido_serializer = PedidoSerializerListar(pedidos, many=True)
        for pedido in pedido_serializer.data:
            id = pedido.get('idPedido')
            ready = Produccion.objects.filter(
                detallePedido__pedido__idPedido=id, estacionActual='empacado' or 'entregado').count()
            goal = Produccion.objects.filter(
                detallePedido__pedido__idPedido=id).count()
            progress = int((ready*100)/goal)
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
            pedido['progressBar'] = {
                "progress": progress, "goal": 100, "color": color}
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
                        paquetes = cantidad['cantidad'] / cantidad['paquete']
                        ultimoPaquete = cantidad['cantidad'] % cantidad['paquete']

                        for i in range(0, int(paquetes)):
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": i+1,
                                "cantidad": cantidad['paquete'],
                                "estacionActual": "creada",
                                "tallaReal": cantidad['talla']
                            }

                            # Guardar la etiqueta
                            produccion_serializer = ProduccionSerializer(
                                data=etiqueta)
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                            else:
                                errors.append(
                                    'No se pudieron generar las etiquetas, error en la solicitud.')
                                success = False

                        # Guardar la última etiqueta
                        if ultimoPaquete > 0:
                            etiqueta = {
                                "detallePedido": newDetalleId,
                                "numEtiqueta": int(paquetes)+1,
                                "cantidad": ultimoPaquete,
                                "estacionActual": "creada",
                                "tallaReal": cantidad['talla']
                            }
                            produccion_serializer = ProduccionSerializer(
                                data=etiqueta)
                            if produccion_serializer.is_valid():
                                produccion_serializer.save()
                            else:
                                errors.append(
                                    'No se pudo generar la última etiqueta, error en la solicitud.')
                                success = False
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


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def pedido_detail_api_view(request, pk=None):
    # queryset
    if request.method == 'GET':
        
        # Obtener el pedido con detalles serializados
        pedido = Pedido.objects.filter(idPedido=pk).first()
        pedido_serializer = PedidoSerializerGetOne(pedido)
        detalles = pedido_serializer.data.get('detalles')

        for detalle in detalles:
            idDetalle = detalle.get('idDetallePedido')
            cantidades = detalle.get('cantidades')
            for cantidad in cantidades:
                
                # Obtener el progreso de cada talla
                progreso_estacion = Produccion.objects \
                    .filter(detallePedido__idDetallePedido=idDetalle, tallaReal=cantidad['talla']) \
                    .values('estacionActual') \
                    .annotate(cuenta=Count('idProduccion'))
                
                # Devolverlo en una matriz
                cantidad['progreso'] = []
                for estacion in progreso_estacion:
                    cantidad['progreso'].append(
                        [estacion['estacionActual'], estacion['cuenta']])

        """
        # objToResponse = {}
        detallesPedido = DetallePedido.objects.filter( pedido__idPedido = pk )

        detallePedido_serializer =  DetallePedidoSerializerGetPedido(detallesPedido,many=True)
        listObjDetalleToResponse = []
        j=0
        for detalle in detallePedido_serializer.data:

            objDetalleToResponse = {}
            idFicha = detalle.get('fichaTecnica').get('idFichaTecnica')
            objDetalleToResponse['idFichaTecnica'] = idFicha
            objDetalleToResponse['nombre'] = detalle.get('fichaTecnica').get('nombre')
            objDetalleToResponse['fotografia'] = detalle.get('fichaTecnica').get('fotografia')
            objDetalleToResponse['talla'] = detalle.get('fichaTecnica').get('talla')
            objDetalleToResponse['ruta'] = detalle.get('rutaProduccion')


            #cantidades tuneadas con progreso
            idDePe = detalle['idDetallePedido']
            arregloCantidades = detalle['cantidades']
            for infoTalla in arregloCantidades:
                talla=infoTalla['talla']
                aux=['tejido','plancha','corte','calidad','empacado']
                i=0
                production=[]
                for dpto in aux:
                    production.insert(i,[dpto,Produccion.objects.filter(detallePedido__idDetallePedido=idDePe,tallaReal=talla,estacionActual=dpto).count()])
                    i=i+1
                objToInsert={"tittle":"Progreso de etiquetas talla "+talla,"data":production}
                infoTalla['progreso']=objToInsert
            
            objDetalleToResponse['cantidades'] = detalle.get('cantidades')
            listObjDetalleToResponse.insert(j,objDetalleToResponse)
            j=j+1

            # Poliesters

            materiales=FichaTecnicaMaterial.objects.filter(fichaTecnica=idFicha , material__tipo='Poliester')
            materiales_serializer = FichaMaterialesSerializerGetPedido(materiales,many=True)
            
            materiales = materiales_serializer.data
            objPoliestersToResponse = []

            
            for material in materiales:
                poliester = {}
                poliester['color'] = material['material']['color']
                poliester['tenida'] = material['material']['tenida']
                poliester['codigoColor'] = material['material']['codigoColor']
                poliester['proveedor'] = material['material']['proveedor']['nombre']
                objPoliestersToResponse.append(poliester)
            

            objDetalleToResponse['poliesters'] = objPoliestersToResponse

            
        objToResponse['pedido'] = pedido_serializer.data.get('idPedido')
        objToResponse['modelo'] = pedido_serializer.data.get('modelo').get('idModelo')
        objToResponse['cliente'] = pedido_serializer.data.get('modelo').get('cliente')
        objToResponse['fechaRegistro'] = pedido_serializer.data.get('fechaRegistro')
        objToResponse['fechaEntrega'] = pedido_serializer.data.get('fechaEntrega')
        #objToResponse['detalles'] =   listObjDetalleToResponse
        """

    return Response(pedido_serializer.data, status=status.HTTP_200_OK)
