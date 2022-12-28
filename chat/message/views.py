from message.models import Message
from rest_framework.generics import ListAPIView
from message.serializers import MessageSerializer
from django.shortcuts import render


class MessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


def index(request):
    return render(request, "chat/index.html")


def room(request, box_id):
    return render(request, "chat/room.html", {"room_name": box_id})
