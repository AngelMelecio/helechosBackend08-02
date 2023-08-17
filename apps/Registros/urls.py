from django.urls import path
from apps.Registros.api import registro_api_view,registro_detail_api_view,regitros_by_idProduccion,produccion_por_modelo_y_empleado
urlpatterns = [
    path('registros/', registro_api_view, name='registro_api_view'),
    path('registro/<int:pk>', registro_detail_api_view, name='registro_detail_api_view'),
    path('progresoByEtiqueta/<int:pk>', regitros_by_idProduccion, name='regitros_by_idProduccion'),
    path('produccion_por_modelo_y_empleado/<str:fechaInicio>/<str:fechaFin>/<str:departamento>', produccion_por_modelo_y_empleado, name='produccion_por_modelo_y_empleado'),
]