from django.urls import path
from apps.DetallePedido.api import detallePedido_api_view,detallePedido_detail_api_view

urlpatterns = [
    path('detallesPedido/', detallePedido_api_view, name='detallePedido_api_view'),
    path('detallesPedido/<int:pk>', detallePedido_detail_api_view, name='detallePedido_detail_api_view'),
]