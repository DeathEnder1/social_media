"""
ASGI config for social_media project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
from facebook_ver2.consumers import ChatConsumer,OnlineStatusConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', ChatConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi())
        ])
    )
})














