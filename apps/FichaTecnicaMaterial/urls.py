from django.urls import path
from apps.FichaTecnicaMaterial.api import ficha_tecnica_material_get_one_api_view,ficha_tecnica_material_post_api_view

urlpatterns = [
    path('fichas_tecnicas_materiales/', ficha_tecnica_material_post_api_view, name='ficha_tecnica_material_post_api_view'),
    path('fichas_tecnicas_materiales/<int:pkFichaTecnica>', ficha_tecnica_material_get_one_api_view, name='ficha_tecnica_material_get_one_api_view'),
]