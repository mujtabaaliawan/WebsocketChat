from user.models import User
from user.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
