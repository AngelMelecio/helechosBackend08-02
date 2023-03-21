from django.urls import path
from apps.Modelos.api import modelo_api_view,modelo_detail_api_view

urlpatterns = [
    path('modelos/', modelo_api_view, name='modelos_api'),
    path('modelos/<int:pk>', modelo_detail_api_view, name='modelo_detail_api_view'),
]