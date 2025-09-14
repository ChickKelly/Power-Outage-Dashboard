"""
ASGI config for power_outage_alert project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import outages.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'power_outage_alert.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            outages.routing.websocket_urlpatterns
        )
    ),
})
