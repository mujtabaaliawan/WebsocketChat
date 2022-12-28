from chatter.models import Chatter
from rest_framework import serializers
from user.serializers import UserSerializer


class ChatterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Chatter
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.get('user')
        user = UserSerializer.create(self, validated_data=user_data)
        mobile_number = validated_data.get('mobile_number')
        chatter, created = Chatter.objects.update_or_create(user=user, mobile_number=mobile_number)
        return chatter
