from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Registros.models import Registro
from apps.Empleados.models import Empleado
from apps.Registros.serializers import RegistroSerializer, RegistroSerializerListar
from apps.Produccion.models import Produccion
from apps.Produccion.serializers import ProduccionSerializerPostRegistro
from apps.Pedidos.models import Pedido
from apps.Pedidos.serializers import PedidoSerializerGetOne
from apps.Empleados.serializers import EmpleadoSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.parsers import JSONParser
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum, Count

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def registro_api_view(request):
    # list
    if request.method == 'GET':
        registros = Registro.objects.all()
        registro_serializer = RegistroSerializerListar(registros, many=True)
        return Response(registro_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':

        registros = request.data
        empleado = Empleado.objects.filter(
            idEmpleado=registros[0].get('empleado')).first()
        empl_srlzr = EmpleadoSerializer(empleado)
        
        fcha = timezone.now()
        unique_pedidos = set()
        rgtrs = []

        for reg in registros:
            # Datos del request
            empl = reg.get('empleado')
            maq = reg.get('maquina')
            dpto = reg.get('departamento')
            trno = reg.get('turno')
            idPrd = reg.get('produccion')

            # Obtenemos el estado actual de la etiqueta
            prd = Produccion.objects.filter(idProduccion=idPrd).first()
            prd_srlzr = ProduccionSerializerPostRegistro(prd)

            estacionAnterior \
                = prd_srlzr.data.get('estacionActual')
            estacionNueva \
                = prd_srlzr.data['detallePedido']['rutaProduccion'][estacionAnterior.lower()]
            mdlo \
                = prd_srlzr.data['detallePedido']['pedido']['modelo']['nombre']
            idPed \
                = prd_srlzr.data['detallePedido']['pedido']['idPedido']
            noEtq \
                = prd_srlzr.data.get('numEtiqueta')

            # Guardamos los pedidos únicos
            unique_pedidos.add(idPed)

            messg = ""
            ok = False

            # validar departamento:
            if (dpto.lower() == estacionAnterior.lower()):
                messg = estacionAnterior + " --> " + estacionNueva
                ok = True
            else:
                messg = "El departamento no coincide con la estacion actual"

            rgtrs.append({
                'modelo': mdlo,
                'numEtiqueta': noEtq,
                'ok': ok,
                'Detalles': messg
            })

            if ok:
                #POST de registro
                reg_serializer = RegistroSerializer(data={
                    'empleado': empl,
                    'maquina': maq,
                    'produccion': idPrd,
                    'turno': trno,
                    'fechaCaptura': fcha,
                    'departamento': dpto
                })
                if reg_serializer.is_valid():
                    reg_serializer.save()

                # PUT de produccion
                prd.estacionActual = estacionNueva
                prd.save()

        response = {
            'empleado': empl_srlzr.data.get('nombre') + " " + empl_srlzr.data.get('apellidos'),
            'fecha': fcha,
            'registros': rgtrs,
            'departamento': registros[0].get('departamento')
        }

        # Enviar las etiquetas actualizadas a los detalles de los pedidos correspondientes
        channel_layer = get_channel_layer()
        for ped in unique_pedidos:
            
            pedido = Pedido.objects.filter(idPedido=ped).first()
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
                        
            dtll_pedido = {
                'type': 'pedido_message',  # This should match the method name in your consumer
                'text': pedido_serializer.data,
            }    
            # Propagacion a través de channels
            async_to_sync(channel_layer.group_send)(f'pedido_{ped}', dtll_pedido)

        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def registro_detail_api_view(request, pk=None):
    # Queryset
    registro = Registro.objects.filter(idRegistro=pk).first()

    # Validacion
    if registro:
        # Retrieve
        if request.method == 'GET':
            registro_serializer = RegistroSerializer(registro)
            return Response(registro_serializer.data, status=status.HTTP_200_OK)

        # Update
        elif request.method == 'PUT':
            registro_serializer = RegistroSerializer(
                registro, data=request.data)
            print('PUTTING')

            if registro_serializer.is_valid():
                registro_serializer.save()
                return Response({'message': '¡Registro actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response(registro_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delete
        elif request.method == 'DELETE':
            registro = Registro.objects.filter(idRegistro=pk).first()
            registro.delete()
            return Response(
                {'message': '¡Registro eliminado correctamente!'},
                status=status.HTTP_200_OK
            )

    return Response(
        {'message': 'No se encontró el registro'},
        status=status.HTTP_400_BAD_REQUEST
    )
