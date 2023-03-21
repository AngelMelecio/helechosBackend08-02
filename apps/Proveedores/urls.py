from django.urls import path
from apps.Proveedores.api import proveedor_api_view,proveedor_detail_api_view

urlpatterns = [
    path('proveedores/', proveedor_api_view, name='proveedores_api'),
    path('proveedores/<int:pk>', proveedor_detail_api_view, name='proveedor_detail_api_view'),
]