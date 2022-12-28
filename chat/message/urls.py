from django.urls import path
from message import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<int:box_id>", views.room, name="chat_room"),
    path("message", views.MessageList.as_view(), name="message_list"),
]
