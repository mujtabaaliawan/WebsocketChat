from rest_framework import serializers
from message.models import Message
from chatter.models import Chatter
from box.models import Box
from chatter.serializers import ChatterSerializer
from box.serializers import BoxSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = ChatterSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Chatter.objects.all(), source='sender', write_only=True)
    box = BoxSerializer(read_only=True)
    box_id = serializers.PrimaryKeyRelatedField(
        queryset=Box.objects.all(), source='box', write_only=True)

    class Meta:
        model = Message
        fields = '__all__'

    # def validate(self, data):
    #     box = data['box']
    #     request = self.context['request']
    #     sender_user_id = request.user.id
    #     sender_id = Chatter.objects.get(user_id=sender_user_id).id
    #     if box.chatter.filter(id=sender_id).exists():
    #         return data
    #     raise serializers.ValidationError("Sender is not added in the box")
