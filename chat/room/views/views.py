from room.models import Room
from room.serializers import RoomSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class RoomCreateList(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomUpdate(RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
