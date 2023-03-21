from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Proveedores.models import Proveedor
from apps.Proveedores.serializers import ProveedorSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def proveedor_api_view(request):
    # list
    if request.method == 'GET':
        proveedores = Proveedor.objects.all()
        proveedor_serializer = ProveedorSerializer(proveedores,many=True)
        return Response( proveedor_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        proveedor_serializer = ProveedorSerializer(data=request.data)
        if proveedor_serializer.is_valid():
            proveedor_serializer.save()
            return Response( {'message':'Proveedor creado correctamente!.'}, status=status.HTTP_201_CREATED )
        return Response( proveedor_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def proveedor_detail_api_view(request, pk=None ):
    # Queryset
    proveedor = Proveedor.objects.filter( idProveedor = pk ).first()
    
    # Validacion
    if proveedor:
        # Retrieve
        if request.method == 'GET':
            proveedor_serializer =  ProveedorSerializer(proveedor)
            return Response( proveedor_serializer.data, status=status.HTTP_200_OK )
        
        # Update
        elif request.method == 'PUT':
            proveedor_serializer = ProveedorSerializer(proveedor, data = request.data)
            print( 'PUTTING' )
            print( request.data )
            if proveedor_serializer.is_valid():
                proveedor_serializer.save()
                return Response( {'message':'Proveedor actualizado correctamente!.'}, status=status.HTTP_200_OK)
            return Response(proveedor_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            proveedor = Proveedor.objects.filter( idProveedor = pk ).first()
            proveedor.delete()
            return Response(
                {'message':'Proveedor eliminado correctamente!.'}, 
                status=status.HTTP_200_OK
            )
    return Response(
        {'message':'No se encontró el proveedor...'}, 
        status=status.HTTP_400_BAD_REQUEST
    )
        