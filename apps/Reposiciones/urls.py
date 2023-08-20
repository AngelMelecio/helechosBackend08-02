from django.urls import path

from apps.Reposiciones.api import reposicion_api_view

urlpatterns = [
    path('reposicion/', reposicion_api_view, name='reposicion_api_post'),
    path('reposicion/<int:fk_produccion>', reposicion_api_view, name='reposicion_api_get'),
]