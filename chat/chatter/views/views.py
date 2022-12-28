from chatter.models import Chatter
from chatter.serializers import ChatterSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class ChatterCreateList(ListCreateAPIView):
    queryset = Chatter.objects.all()
    serializer_class = ChatterSerializer


class ChatterUpdate(RetrieveUpdateAPIView):
    queryset = Chatter.objects.all()
    serializer_class = ChatterSerializer
