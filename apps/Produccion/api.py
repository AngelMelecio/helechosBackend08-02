from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from apps.Produccion.models import Produccion
from apps.Produccion.serializers import ProduccionSerializer, ProduccionSerializerListar
from rest_framework.parsers import MultiPartParser, JSONParser

@api_view(['GET','POST'])
@parser_classes([MultiPartParser , JSONParser])
def produccion_api_view(request):
    # list
    if request.method == 'GET':
        listaProduccion = Produccion.objects.all()
        produccion_serializer = ProduccionSerializerListar(listaProduccion,many=True)
        return Response( produccion_serializer.data, status=status.HTTP_200_OK )

    # Create
    elif request.method == 'POST':
        produccion_serializer = ProduccionSerializer(data=request.data)
        if produccion_serializer.is_valid():
            produccion_serializer.save()
            return Response( {
                'message':'¡Registro de producción creado correctamente!',
            }, status=status.HTTP_201_CREATED )
        return Response( produccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['PUT'])
@parser_classes([MultiPartParser, JSONParser])
def update_produccion_impresion(request):
    data = request.data
    try:
        for i in data:
            id = i.get('idProduccion', None)
            obj = Produccion.objects.get(idProduccion=id)
            if obj.estacionActual == 'creada' :
               obj.fechaImpresion = timezone.now() 
               obj.estacionActual = 'tejido'
                
            obj.save()
    except Produccion.DoesNotExist:
        return Response( {
            'message':'¡Registro de producción no encontrado!',
        }, status=status.HTTP_400_BAD_REQUEST )
    return Response( {
        'message':'¡Registros de producción actualizados correctamente!'
    }, status=status.HTTP_200_OK )


@api_view(['GET'])
@parser_classes([MultiPartParser, JSONParser])
def get_produccion_with_registros_by_pedido(request, pk=None):#idDetalleProduccion
    # Queryset
    etiquetas = Produccion.objects.filter(detallePedido__pedido__idPedido = pk )

    # Validacion
    if etiquetas:
        etiquetasSerializadas =  ProduccionSerializerListar(etiquetas, many=True)
        objToResponse = []
        total=len(etiquetasSerializadas.data)

        

        for etiqueta in etiquetasSerializadas.data:
            colores=""
            for color in etiqueta['detallePedido']['fichaTecnica']['materiales']:
                colores+=color['color']+"\n"
            colores=colores[:-3]

            objToResponse.append({
                'idProduccion':etiqueta['idProduccion'],
                'idPedido':etiqueta['detallePedido']['pedido'],
                'modelo':etiqueta['detallePedido']['fichaTecnica']['modelo']['nombre'],
                'color':colores,
                'talla':etiqueta['tallaReal'],
                'cantidad':etiqueta['cantidad'],
                'numEtiqueta':(etiqueta['numEtiqueta']+"/"+str(total)),
                'estado' :"No impresa" if etiqueta['fechaImpresion'] is None else "Impresa",
                'rutaProduccion':etiqueta['detallePedido']['rutaProduccion'],
                'estacionActual':etiqueta['estacionActual'],
                'idDetallePedido':etiqueta['detallePedido']['idDetallePedido'],
            })

        return Response( objToResponse, status=status.HTTP_200_OK )
    
    return Response(
        {'message':'No se encontraron etiquetas relacionadas'}, 
        status=status.HTTP_400_BAD_REQUEST
    )