from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Empleados.models import Empleado
from apps.Empleados.serializers import EmpleadoSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def empleado_api_view(request):
    # list
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        empleados_serializer = EmpleadoSerializer(empleados,many=True)
        return Response( empleados_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        empleado_serializer = EmpleadoSerializer(data=request.data)
        if empleado_serializer.is_valid():
            empleado_serializer.save()
            return Response( {
                'message':'Empleado creado correctamente!.',
                'empleado': empleado_serializer.data
            }, status=status.HTTP_201_CREATED )
        return Response( empleado_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def empleado_detail_api_view(request, pk=None):
    # Queryset
    empleado = Empleado.objects.filter( idEmpleado = pk ).first()
    
    # Validacion
    if empleado:
        # Retrieve
        if request.method == 'GET':
            empleado_serializer =  EmpleadoSerializer(empleado)
            return Response( empleado_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            empleado_serializer = EmpleadoSerializer(empleado, data = request.data)
            print( 'PUTTING' )
            print( request.data )
            if empleado_serializer.is_valid():
                empleado_serializer.save()
                return Response( {'message':'Empleado actualizado correctamente!.'}, status=status.HTTP_200_OK)
            return Response(empleado_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            empleado = Empleado.objects.filter( idEmpleado = pk ).first()
            empleado.delete()
            return Response(
                {'message':'Empleado eliminado correctamente!.'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el empleado...'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
 