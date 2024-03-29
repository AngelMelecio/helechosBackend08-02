from django.urls import path
from apps.FichaTecnicaMaterial.api import ficha_tecnica_material_post_api_view,materiales_by_fichaTecnica,materiales_by_pedido

urlpatterns = [
    path('fichas_tecnicas_materiales/', ficha_tecnica_material_post_api_view, name='ficha_tecnica_material_post_api_view'),
    path('materiales_by_fichaTecnica/<int:pkFichaTecnica>', materiales_by_fichaTecnica, name='materiales_by_fichaTecnica'),
    path('materiales_by_pedido/<int:pkPedido>', materiales_by_pedido, name='materiales_by_pedido'),
]