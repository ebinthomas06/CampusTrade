# In campus_mart/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import api.routing # We will create this file next

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_mart.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles standard HTTP requests
    "websocket": AuthMiddlewareStack( # Handles WebSocket requests
        URLRouter(
            api.routing.websocket_urlpatterns
        )
    ),
})