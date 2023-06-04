from django.urls import path
from apps.Pedidos.api import pedido_api_view,pedido_detail_api_view
urlpatterns = [
    path('pedidos/', pedido_api_view, name='pedido_api_view'),
    path('pedidos/<int:pk>', pedido_detail_api_view, name='pedido_detail_api_view'),
]