from rest_framework import serializers
from room.models import Room
from chatter.models import Chatter
from chatter.serializers import ChatterSerializer


class RoomSerializer(serializers.ModelSerializer):
    owner = ChatterSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = Chatter.objects.get(user_id=request.user.id)
        return super().create(validated_data)
