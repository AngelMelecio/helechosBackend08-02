from django.urls import path
from apps.EmpleadoMaquina.api import empleado_maquina_api_view,empleado_maquina_detail_api_view,empleado_maquinas_api_view

urlpatterns = [
    path('empleados_maquina/', empleado_maquina_api_view, name='empleados_maquina_api'),
    path('empleados_maquina/<int:pkEmpleado>', empleado_maquina_detail_api_view, name='empleado_maquina_detail_api_view'),
    path('empleado_maquinas/', empleado_maquinas_api_view, name='empleado_maquinas_api_view')

]