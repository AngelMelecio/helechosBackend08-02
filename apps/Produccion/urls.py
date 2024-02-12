from django.urls import path
from apps.Produccion.api import produccion_api_view,update_produccion_impresion,get_produccion_with_registros_by_pedido,create_reposicion_or_extra

urlpatterns = [
    path('produccion/', produccion_api_view, name='produccion_api_view'),
    path('produccionPrint/', update_produccion_impresion, name='update_produccion_impresion'),
    path('produccionByPedido/<int:pk>', get_produccion_with_registros_by_pedido, name="get_produccion_with_registros_by_detallePedido"),
    path('produccionReposicionExtra/', create_reposicion_or_extra, name="create_reposicion_or_extra")
]