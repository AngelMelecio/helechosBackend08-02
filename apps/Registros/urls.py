from django.urls import path
from apps.Registros.api import registro_api_view,registro_detail_api_view,regitros_by_idProduccion
urlpatterns = [
    path('registros/', registro_api_view, name='registro_api_view'),
    path('registro/<int:pk>', registro_detail_api_view, name='registro_detail_api_view'),
    path('progresoByEtiqueta/<int:pk>', regitros_by_idProduccion, name='regitros_by_idProduccion'),
]