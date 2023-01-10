from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from box.models import Box
from box.serializers import BoxSerializer, InductionSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from box.permissions import box_update_permission
from rest_framework.views import APIView


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


class BoxDetail(APIView):

    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        box_id = self.kwargs["box_id"]
        return JsonResponse(data=Box.objects.get(id=box_id).box_detail)
