from django.urls import path
from apps.Maquinas.api import maquina_api_view,maquina_detail_api_view

urlpatterns = [
    path('maquinas/', maquina_api_view, name='maquinas_api'),
    path('maquinas/<int:pk>', maquina_detail_api_view, name='maquina_detail_api_view'),
]