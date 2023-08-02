from django.urls import path
from apps.Modelos.api import modelo_api_view,modelo_detail_api_view, modelos_cliente_api_view 


urlpatterns = [
    path('modelos/', modelo_api_view, name='modelo_api_view'),
    path('modelos/<int:pk>', modelo_detail_api_view, name='modelo_detail_api_view'),
    path('modelos_cliente/<int:pk>', modelos_cliente_api_view, name='modelo_detail_api_view'),
]