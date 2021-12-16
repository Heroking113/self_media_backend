"""
ASGI config for cb_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import apps.chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cb_backend.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    # http请求使用这个
    "http": get_asgi_application(),

    # websocket请求使用这个
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})