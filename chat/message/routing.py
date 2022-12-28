from django.urls import re_path
from message import consumers


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<box_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
