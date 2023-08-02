from django.urls import path
from apps.Produccion.api import produccion_api_view,update_produccion_impresion,get_produccion_with_registros_by_pedido

urlpatterns = [
    path('produccion/', produccion_api_view, name='produccion_api_view'),
    path('produccionPrint/', update_produccion_impresion, name='update_produccion_impresion'),
    path('produccionByPedido/<int:pk>', get_produccion_with_registros_by_pedido, name="get_produccion_with_registros_by_detallePedido")
]