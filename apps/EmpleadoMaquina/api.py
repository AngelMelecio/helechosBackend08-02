from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.EmpleadoMaquina.models import EmpleadoMaquina
from apps.EmpleadoMaquina.serializers import EmpleadoMaquinaSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


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
        empleadoMaquina_serializer = EmpleadoMaquinaSerializer( data=request.data)
        if empleadoMaquina_serializer.is_valid():
            empleadoMaquina_serializer.save()
            return Response({'message': 'Maquinas asignadas correctamente!.'}, status=status.HTTP_201_CREATED)
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
                {'message': 'Se quitaron las maquinas al empleado!.'},
                status=status.HTTP_200_OK
            )
    return Response(
        {'message': 'No se encontraron maquinas relacionadas...'},
        status=status.HTTP_200_OK
    )
