from box.models import Box
from box.serializers import BoxSerializer, InductionSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from box.permissions import box_update_permission


class BoxCreateList(ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class BoxUpdate(RetrieveUpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    permission_classes = (box_update_permission.IsOwner,)


class InductionUpdate(RetrieveUpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = InductionSerializer
