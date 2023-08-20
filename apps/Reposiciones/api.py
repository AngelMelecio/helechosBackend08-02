from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from apps.Reposiciones.serilizers import ReposicionSerilizer,ReposicionSerilizerGet
from apps.Reposiciones.models import Reposicion

@api_view(["POST", "GET"])
@parser_classes([MultiPartParser, JSONParser])
def reposicion_api_view(request, fk_produccion=None):
    if request.method == 'POST':

        rpscn_srlzr = ReposicionSerilizer(data=request.data)
        if rpscn_srlzr.is_valid():
            rpscn_srlzr.save()
            rpscns = Reposicion.objects.filter( produccion = request.data['produccion'] )
            rpscn_srlzr = ReposicionSerilizerGet(rpscns, many=True)
            return Response({
                'reposiciones': rpscn_srlzr.data,
                'message':'¡Reposición creada correctamente!',
            }, status=status.HTTP_201_CREATED)
    
        return Response({
            'message':'¡Error al crear reposición!',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        rpscns = Reposicion.objects.filter(produccion = fk_produccion)
        rpscn_srlzr = ReposicionSerilizerGet(rpscns, many=True)
        return Response({
            'reposiciones': rpscn_srlzr.data,
        }, status=status.HTTP_200_OK)
    
    return Response({
        'message': "¡Error en la solicitud!",
    }, status=status.HTTP_400_BAD_REQUEST)