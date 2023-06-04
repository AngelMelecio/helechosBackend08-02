from django.urls import path
from apps.Produccion.api import produccion_api_view,produccion_detail_api_view

urlpatterns = [
    path('produccion/', produccion_api_view, name='produccion_api_view'),
    path('produccion/<int:pk>', produccion_detail_api_view, name='produccion_detail_api_view'),
]