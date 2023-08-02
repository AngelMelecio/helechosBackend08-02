from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Registros.models import Registro
from apps.Empleados.models import Empleado
from apps.Registros.serializers import RegistroSerializer, RegistroSerializerListar,RegistroSerializerToChart
from apps.Produccion.serializers import ProduccionSerializer
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
        cambios_pedido = {}
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

            mdlo \
                = prd_srlzr.data['detallePedido']['pedido']['modelo']['nombre']
            idPed \
                = prd_srlzr.data['detallePedido']['pedido']['idPedido']
            noEtq \
                = prd_srlzr.data.get('numEtiqueta')
            tll \
                = prd_srlzr.data.get('tallaReal')
            idDtllPed \
                = prd_srlzr.data['detallePedido']['idDetallePedido']
            rta \
                = prd_srlzr.data['detallePedido']['rutaProduccion']
            estacionAnterior \
                = prd_srlzr.data.get('estacionActual')
            estacionNueva \
                = rta[estacionAnterior.lower()]

            ok = False
            messg = "La etiqueta aún no ha sido escaneada en " + estacionAnterior + '.'
            pos = "creada"

            # validar departamento:
            while pos != estacionAnterior.lower() : 
                pos = rta[pos]
                if( pos == dpto.lower() ):
                    if (dpto.lower() == estacionAnterior.lower()):
                        messg = estacionAnterior + " --> " + estacionNueva
                        ok = True
                    else :
                        messg = 'La etiqueta ya ha sido escaneada en ' + dpto + '.'
                    break

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
                else:
                    print(reg_serializer.errors)

                # PUT de produccion
                prd.estacionActual = estacionNueva
                prd.save()

                # Cambios para sockets
                if not idPed in cambios_pedido:
                    cambios_pedido[idPed] = []

                cambios_pedido[idPed].append({
                    'produccion': idPrd,
                    'detallePedido': idDtllPed,
                    'talla' : tll,
                    'estacionNueva': estacionNueva,
                })

        response = {
            'empleado': empl_srlzr.data.get('nombre') + " " + empl_srlzr.data.get('apellidos'),
            'fecha': fcha,
            'registros': rgtrs,
            'departamento': registros[0].get('departamento')
        }

        # Enviar los cambios en la producciónn a los pedidos correspondientes
        channel_layer = get_channel_layer()
        for ped, details in cambios_pedido.items():
            dtll_pedido = {
                'type': 'pedido_message',  # This should match the method name in your consumer
                'text': details,
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

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def regitros_by_idProduccion(request, pk=None):
    # Queryset
    etiqueta = Produccion.objects.filter(idProduccion=pk).first()

    # Validacion
    if etiqueta:
        registros = Registro.objects.filter(produccion=pk).order_by('fechaCaptura')
        registros_serializer = RegistroSerializerToChart(registros, many=True)  
        objToResponse = [] 
        it=1 
        fechaAnterior = etiqueta.fechaImpresion
        n = len(registros_serializer.data)
        for registro in registros_serializer.data:
            item=[]
            maquina = ' N/A'
            if not registro['maquina'] == None:
                maquina = ' - M' + registro['maquina']['numero'] + '  L' + registro['maquina']['numero']
            item.append(registro['departamento'])
            item.append(registro['empleado']['nombre'] + ' ' + registro['empleado']['apellidos']+maquina)
            item.append(fechaAnterior)
            if it == n:
                item.append(timezone.now())
            else:
                item.append(registro['fechaCaptura'])

            it=it+1
            fechaAnterior = registro['fechaCaptura']
            objToResponse.append(item)
        return Response(objToResponse, status=status.HTTP_200_OK)

      

    return Response(
        {'message': 'Registro de producción no encontrado'},
        status=status.HTTP_400_BAD_REQUEST
    )
