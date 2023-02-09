from django.urls import path
from apps.Empleados.api import empleado_api_view,empleado_detail_api_view

urlpatterns = [
    path('empleados/', empleado_api_view, name='empleados_api'),
    path('empleados/<int:pk>', empleado_detail_api_view, name='empleado_detail_api_view'),
]