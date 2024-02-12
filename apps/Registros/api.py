from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Registros.models import Registro
from apps.Empleados.models import Empleado
from apps.Registros.serializers import RegistroSerializer, RegistroSerializerListar, RegistroSerializerToChart
from apps.Produccion.models import Produccion
from apps.Produccion.serializers import ProduccionSerializerPostRegistro
from apps.Empleados.serializers import EmpleadoSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.parsers import JSONParser
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum, Case, When, IntegerField, F


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
        empleado = Empleado.objects.filter(idEmpleado=registros[0].get('empleado')).first()
        empl_srlzr = EmpleadoSerializer(empleado)
        fcha = timezone.now()
        cambios_pedido = {}
        rgtrs = []

        for reg in registros:

            # Datos del request
            empl = reg.get('empleado')
            maq = reg.get('maquina')
            dpto = empl_srlzr.data.get('departamento')
            trno = reg.get('turno')
            idPrd = reg.get('produccion')

            # Obtenemos el estado actual de la etiqueta
            prd = Produccion.objects.filter(idProduccion=idPrd).first()
            prd_srlzr = ProduccionSerializerPostRegistro(prd)

            mdlo = prd_srlzr.data['detallePedido']['pedido']['modelo']['nombre']
            idPed = prd_srlzr.data['detallePedido']['pedido']['idPedido']
            noEtq = prd_srlzr.data.get('numEtiqueta')
            tll = prd_srlzr.data.get('tallaReal')
            idDtllPed = prd_srlzr.data['detallePedido']['idDetallePedido']
            rta = prd_srlzr.data['detallePedido']['rutaProduccion']
            estacionAnterior = prd_srlzr.data.get('estacionActual')
            tipo = prd_srlzr.data['tipo']
            destino = rta[prd_srlzr.data['destino']] if tipo == 'Reposicion' else None

            if not estacionAnterior == "empacado":
                estacionNueva = rta[estacionAnterior.lower()]

                ok = False
                messg = "La etiqueta aún no ha sido escaneada en " + estacionAnterior + '.'
                pos = "creada"

                if tipo == 'Reposicion' and destino.lower() == dpto.lower():

                    messg = 'Esta etiqueta no se puede seguir escaneando, ya llegó a su destino: ' + prd_srlzr.data['destino'] + '.'
                else:
                    # validar departamento:
                    while pos != estacionAnterior.lower():
                        pos = rta[pos]
                        if (pos == dpto.lower()):
                            if (dpto.lower() == estacionAnterior.lower()):
                                messg = estacionAnterior + " --> " + estacionNueva
                                ok = True
                            else:
                                messg = 'La etiqueta ya ha sido escaneada en ' + dpto + '.'
                            break

                rgtrs.append({
                    'modelo': mdlo,
                    'numEtiqueta': noEtq,
                    'ok': ok,
                    'Detalles': messg
                })

                if ok:
                    # POST de registro
                    reg_serializer = RegistroSerializer(data={
                        'empleado': empl,
                        'maquina': maq,
                        'produccion': idPrd,
                        'turno': trno,
                        'fechaCaptura': fcha,
                        'departamento': dpto,
                        'tipo':tipo

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
                        'talla': tll,
                        'estacionNueva': estacionNueva,
                    })
            else:
                rgtrs.append({
                    'modelo': mdlo,
                    'numEtiqueta': noEtq,
                    'ok': False,
                    'Detalles': 'La etiqueta ya ha sido escaneada en Empaque.'
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
            async_to_sync(channel_layer.group_send)(
                f'pedido_{ped}', dtll_pedido)

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
        registros = Registro.objects.filter(
            produccion=pk).order_by('fechaCaptura')
        registros_serializer = RegistroSerializerToChart(registros, many=True)
        objToResponse = []
        it = 1
        fechaAnterior = etiqueta.fechaImpresion
        n = len(registros_serializer.data)
        for registro in registros_serializer.data:
            item = []
            maquina = ' N/A'
            if not registro['maquina'] == None:
                maquina = ' L' + \
                    registro['maquina']['linea'] + ' - M' + \
                    registro['maquina']['numero']
            item.append(registro['departamento'])
            item.append(registro['empleado']['nombre'] +
                        ' ' + registro['empleado']['apellidos']+maquina)
            item.append(fechaAnterior)
            if it == n:
                item.append(timezone.now())
            else:
                item.append(registro['fechaCaptura'])

            it = it+1
            fechaAnterior = registro['fechaCaptura']
            objToResponse.append(item)
        return Response(objToResponse, status=status.HTTP_200_OK)
    return Response(
        {'message': 'Registro de producción no encontrado'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def produccion_por_modelo_y_empleado(request, fechaInicio, fechaFin, departamento):
    # Consulta mejorada
    producciones = (Registro.objects
                    .filter(departamento=departamento, fechaCaptura__range=(fechaInicio, fechaFin))
                    .values('empleado__nombre', 'empleado__apellidos', 
                            'produccion__detallePedido__fichaTecnica__modelo__nombre')
                    .annotate(
                        ordinario=Sum(Case(When(tipo='Ordinario', then='produccion__cantidad'), 
                                            output_field=IntegerField())),
                        extra=Sum(Case(When(tipo='Extra', then='produccion__cantidad'), 
                                            output_field=IntegerField())),
                        reposicion=Sum(Case(When(tipo='Reposicion', then='produccion__cantidad'), 
                                       output_field=IntegerField())),
                        falla=Sum(Case(When(tipo='Falla', then='produccion__cantidad'), 
                                       output_field=IntegerField()))
                    )
                    .order_by('empleado__nombre', 'empleado__apellidos', 
                              'produccion__detallePedido__fichaTecnica__modelo__nombre'))

    # Construcción del objeto de datos
    data = []
    empleados = set([prod['empleado__nombre'] + " " + prod['empleado__apellidos'] for prod in producciones])

    for empleado in empleados:
        emp_data = {
            "empleado": empleado,
            "modelos": []
        }

        modelos_empleado = [prod for prod in producciones if prod['empleado__nombre'] + " " + prod['empleado__apellidos'] == empleado]

        for modelo_data in modelos_empleado:
            modelo_obj = {
                "modelo": modelo_data['produccion__detallePedido__fichaTecnica__modelo__nombre'],
                "ordinario": modelo_data['ordinario'],
                "extra": modelo_data['extra'],
                "reposicion": modelo_data['reposicion'],
                "falla": modelo_data['falla']
                
            }

            emp_data['modelos'].append(modelo_obj)

        data.append(emp_data)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def produccion_por_maquina_y_turno(request, fechaInicio, fechaFin, departamento):
    # Ajusta la consulta para sumar por tipos de turno y producción, ajustando por fallas
    registros = (Registro.objects
                .filter(departamento=departamento, fechaCaptura__range=(fechaInicio, fechaFin))
                .values('maquina__linea', 'maquina__numero')
                .annotate(
                    m=Sum(Case(When(tipo='Ordinario', turno='Mañana', then='produccion__cantidad'),
                                When(tipo='Extra', turno='Mañana', then='produccion__cantidad'),
                                When(tipo='Reposicion', turno='Mañana', then='produccion__cantidad'),
                                When(tipo='Falla', turno='Mañana', then=F('produccion__cantidad') * -1),
                                default=0,
                                output_field=IntegerField())),
                    t=Sum(Case(When(tipo='Ordinario', turno='Tarde', then='produccion__cantidad'),
                                When(tipo='Extra', turno='Tarde', then='produccion__cantidad'),
                                When(tipo='Reposicion', turno='Tarde', then='produccion__cantidad'),
                                When(tipo='Falla', turno='Tarde', then=F('produccion__cantidad') * -1),
                                default=0,
                                output_field=IntegerField())),
                    n=Sum(Case(When(tipo='Ordinario', turno='Noche', then='produccion__cantidad'),
                                When(tipo='Extra', turno='Noche', then='produccion__cantidad'),
                                When(tipo='Reposicion', turno='Noche', then='produccion__cantidad'),
                                When(tipo='Falla', turno='Noche', then=F('produccion__cantidad') * -1),
                                default=0,
                                output_field=IntegerField()))
                )
                .order_by('maquina__linea', 'maquina__numero'))

    data = list(registros)

    return Response(data, status=status.HTTP_200_OK)