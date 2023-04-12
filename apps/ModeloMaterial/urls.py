from django.urls import path
from apps.ModeloMaterial.api import modelo_material_post_api_view, modelo_material_get_one_api_view

urlpatterns = [
    path('modelo_material/', modelo_material_post_api_view, name='modelo_material_post_api'),
    path('modelo_material/<int:pkModelo>', modelo_material_get_one_api_view, name='modelo_material_get_one_api')
]