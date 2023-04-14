from django.urls import path
from apps.FichasTecnicas.api import ficha_tecnica_api_view,ficha_tecnica_detail_api_view,ficha_tecnica_get_for_model

urlpatterns = [
    path('fichas_tecnicas/', ficha_tecnica_api_view, name='ficha_tecnica_api_view'),
    path('fichas_tecnicas/<int:pk>', ficha_tecnica_detail_api_view, name='ficha_tecnica_detail_api_view'),
    path('fichas_tecnicas_modelo/<int:pkModelo>', ficha_tecnica_get_for_model, name='ficha_tecnica_get_for_model'),
]