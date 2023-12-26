from django.urls import path
from apps.TiposMateriales.api import tiposMateriales_api_view,tiposMateriales_detail_api_view

urlpatterns = [
    path('tiposMaterialess/', tiposMateriales_api_view, name='tiposMaterialess_api'),
    path('tiposMaterialess/<int:pk>', tiposMateriales_detail_api_view, name='tiposMateriales_detail_api_view'),
]