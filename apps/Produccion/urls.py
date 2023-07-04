from django.urls import path
from apps.Produccion.api import produccion_api_view,produccion_detail_api_view,get_produccion_with_registros_by_pedido

urlpatterns = [
    path('produccion/', produccion_api_view, name='produccion_api_view'),
    path('produccion/<int:pk>', produccion_detail_api_view, name='produccion_detail_api_view'),
    path('produccionByPedido/<int:pk>', get_produccion_with_registros_by_pedido, name="get_produccion_with_registros_by_detallePedido")
]