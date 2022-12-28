from rest_framework import serializers
from box.models import Box
from room.models import Room
from chatter.models import Chatter
from room.serializers import RoomSerializer
from chatter.serializers import ChatterSerializer


class BoxSerializer(serializers.ModelSerializer):
    chatter = ChatterSerializer(read_only=True, many=True)
    owner = ChatterSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(),
                                                 source='room', write_only=True)

    class Meta:
        model = Box
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = Chatter.objects.get(user_id=request.user.id)
        return super().create(validated_data)


class InductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'chatter']

    def update(self, instance, validated_data):
        chatters_to_add = validated_data["chatter"]
        for chatter in chatters_to_add:
            instance.chatter.add(chatter)
        return instance
