from django.urls import path
from apps.Clientes.api import cliente_api_view,cliente_detail_api_view

urlpatterns = [
    path('clientes/', cliente_api_view, name='clientes_api'),
    path('clientes/<int:pk>', cliente_detail_api_view, name='cliente_detail_api_view'),
]