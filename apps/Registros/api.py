from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Registros.models import Registro
from apps.Empleados.models import Empleado
from apps.Registros.serializers import RegistroSerializer, RegistroSerializerListar
from apps.Produccion.models import Produccion
from apps.Empleados.serializers import EmpleadoSerializer
from apps.Produccion.serializers import ProduccionSerializerPostRegistro
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.parsers import JSONParser
from django.utils import timezone


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
        fcha = timezone.now()
        empleado = Empleado.objects.filter(
            idEmpleado=registros[0].get('empleado')).first()
        empl_srlzr = EmpleadoSerializer(empleado)
        

        rgtrs = []
        for reg in registros:
            # Obtenemos el estado actual de la etiqueta
            idPrd = reg.get('produccion')
            prd = Produccion.objects.filter(idProduccion=idPrd).first()
            prd_srlzr = ProduccionSerializerPostRegistro(prd)
            
            empl = reg.get('empleado')
            maq = reg.get('maquina')
            dpto = reg.get('departamento')
            trno = reg.get('turno')

            estacionAnterior \
                = prd_srlzr.data.get('estacionActual')
            estacionNueva \
                = prd_srlzr.data['detallePedido']['rutaProduccion'][estacionAnterior.lower()]
            modelo \
                = prd_srlzr.data['detallePedido']['pedido']['modelo']['nombre']

            messg = ""
            ok = False

            # validar departamento:
            if (dpto.lower() == estacionAnterior.lower()):
                messg = estacionAnterior + " --> " + estacionNueva
                ok = True
            else:
                messg = "El departamento no coincide con la estacion actual"

            rgtrs.append({
                'modelo': modelo,
                'numEtiqueta': prd_srlzr.data.get('numEtiqueta'),
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

        return Response(response, status=status.HTTP_200_OK)
        """
            if p_s.is_valid() :
            else:
                print( p_s.errors )

        registro_serializer = RegistroSerializer(data=request.data)
        if registro_serializer.is_valid():
            registro_serializer.save()
            return Response( {'message':'¡Registro creado correctamente!'}, status=status.HTTP_201_CREATED )
        return Response( registro_serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        """


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
