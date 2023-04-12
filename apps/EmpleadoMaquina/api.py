from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.EmpleadoMaquina.models import EmpleadoMaquina
from apps.EmpleadoMaquina.serializers import EmpleadoMaquinaSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction

@transaction.atomic
@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
def empleado_maquinas_api_view(request):
    if request.method == 'POST':
        sid = transaction.savepoint()

        empleado = request.data.get('idEmpleado')
        maquinas = request.data.get('maquinas')
        success = True

        EmpleadoMaquina.objects.select_for_update().filter( idEmpleado = empleado ).delete()
        for m in maquinas:
            empleado_maquina = { 'idEmpleado':empleado, 'idMaquina':m.get('id') }
            empleadoMaquina_serializer = EmpleadoMaquinaSerializer( data=empleado_maquina )
            if empleadoMaquina_serializer.is_valid():
                empleadoMaquina_serializer.save()
            else:
                success = False
        if success:
            transaction.savepoint_commit(sid)
            return Response({'message':'¡Asignación correcta de máquinas!'}, status=status.HTTP_200_OK)
        else:
            transaction.savepoint_rollback(sid)
            return Response({'message':'Ha ocurrido un error durante la asignación de maquinas'}, status=status.HTTP_409_CONFLICT)

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, JSONParser])
def empleado_maquina_api_view(request):
    # list
    if request.method == 'GET':
        empleadoMaquinas = EmpleadoMaquina.objects.all()
        empleadoMaquina_serializer = EmpleadoMaquinaSerializer(empleadoMaquinas, many=True)
        return Response(empleadoMaquina_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':
        empleadoMaquina_serializer = EmpleadoMaquinaSerializer( data=request.data )
        if empleadoMaquina_serializer.is_valid():
            empleadoMaquina_serializer.save()
            return Response({'message': '¡Máquinas asignadas correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(empleadoMaquina_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def empleado_maquina_detail_api_view(request, pkEmpleado):
    # Queryset
    empleadoMaquina = EmpleadoMaquina.objects.filter(idEmpleado=pkEmpleado)
    # Validacion
    if empleadoMaquina:
        # Retrieve
        if request.method == 'GET':
            empleadoMaquina_serializer = EmpleadoMaquinaSerializer(empleadoMaquina, many=True)
            return Response(empleadoMaquina_serializer.data, status=status.HTTP_200_OK)

        # Delete
        elif request.method == 'DELETE':
            empleadoMaquina = EmpleadoMaquina.objects.filter(idEmpleado=pkEmpleado)
            empleadoMaquina.delete()
            return Response(
                {'message': '¡Se quitaron las máquinas al empleado!'},
                status=status.HTTP_200_OK
            )
    return Response(
        {'message': 'No se encontraron maquinas relacionadas'},
        status=status.HTTP_200_OK
    )
