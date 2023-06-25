from django.urls import path
from apps.FichasTecnicas.api import ficha_tecnica_api_view,ficha_tecnica_detail_api_view,fichas_tecnicas_with_materials_view,fichas_by_modelo

urlpatterns = [
    path('fichas_tecnicas/', ficha_tecnica_api_view, name='ficha_tecnica_api_view'),
    path('fichas_tecnicas/<int:pk>', ficha_tecnica_detail_api_view, name='ficha_tecnica_detail_api_view'),
    path('fichas_tecnicas_materiales/<int:pk>', fichas_tecnicas_with_materials_view, name='fichas_tecnicas_with_materials_view'),
    path('fichas_by_modelo/<int:pk>', fichas_by_modelo, name='fichas_by_modelo')

]