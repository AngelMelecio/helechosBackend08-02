"""
ASGI config for backendHelechos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import re_path

from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from apps.Pedidos.consumers import PedidosConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendHelechos.settings.local')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/pedidos/(?P<pedido_id>\w+)/$', PedidosConsumer.as_asgi()),
                
            ])
        ) 
    ),
})