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
