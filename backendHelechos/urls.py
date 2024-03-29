
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path,re_path
from django.views.static import serve

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.Users.views import Login,Logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.Clientes.urls')),
    path('api/', include('apps.Materiales.urls')),
    path('api/', include('apps.Modelos.urls')),
    path('api/', include('apps.Proveedores.urls')),
    path('api/', include('apps.Empleados.urls')),
    path('api/', include('apps.Maquinas.urls')),
    path('api/', include('apps.EmpleadoMaquina.urls')),
    path('api/', include('apps.FichasTecnicas.urls')),
    path('api/', include('apps.FichaTecnicaMaterial.urls')),
    path('api/', include('apps.Pedidos.urls')),
    path('api/', include('apps.DetallePedido.urls')),
    path('api/', include('apps.Produccion.urls')),
    path('api/', include('apps.Registros.urls')),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('login/',Login.as_view(), name = 'login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/',include('apps.Users.routers')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
