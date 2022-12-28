# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from box.models import Box
from message.models import Message
from message.serializers import MessageSerializer
from chatter.models import Chatter
from box.serializers import BoxSerializer


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.box_id = self.scope["url_route"]["kwargs"]["box_id"]
        self.room_group_name = "chat_%s" % self.box_id


        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        user = self.scope["user"]
        chatter_id = Chatter.objects.get(user_id=user).id
        box_id = self.scope["url_route"]["kwargs"]["box_id"]
        box = Box.objects.get(id=box_id)
        if box.chatter.filter(id=chatter_id).exists():
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            self.create_message(message)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
        else:
            raise PermissionError("You are not Permitted in this box")

    # Receive message from room group
    def chat_message(self, message):
        message_list = self.get_message_from_list()
        for message_id in message_list:
            message = Message.objects.get(id=message_id)
        # Send message to WebSocket
            self.send(text_data=json.dumps({"message": message.message}))
        self.clear_unread_messages()

    # Create new message
    def create_message(self, message):

        user = self.scope["user"]
        box_id = self.scope["url_route"]["kwargs"]["box_id"]
        serializer = MessageSerializer(data={"message": message,
                                             "sender_id": user.id,
                                             "box_id": box_id})
        serializer.is_valid()
        new_message = serializer.save()
        self.add_in_list(message=new_message)

    def add_in_list(self, message):
        box = message.box
        msg_check_list = box.unread_messages

        for chatter in message.box.chatter.all():
            chatter_id = chatter.id
            chatter_id_str = f"{chatter_id}"
            msg_check_list.setdefault(chatter_id_str, [])
            msg_check_list[chatter_id_str].append(message.id)
        serializer = BoxSerializer(box, data={"unread_messages": msg_check_list}, partial=True)
        if serializer.is_valid():
            serializer.save()

    def get_message_from_list(self):
        user = self.scope["user"]
        box_id = self.scope["url_route"]["kwargs"]["box_id"]
        box = Box.objects.get(id=box_id)
        chatter_id = Chatter.objects.get(user_id=user.id).id
        unread_messages_list = box.unread_messages
        chatter_id_str = f"{chatter_id}"
        unread_messages = unread_messages_list[chatter_id_str]
        return unread_messages

    def clear_unread_messages(self):
        user = self.scope["user"]
        chatter_id = Chatter.objects.get(user_id=user.id).id
        box_id = self.scope["url_route"]["kwargs"]["box_id"]
        box = Box.objects.get(id=box_id)
        unread_messages_list = box.unread_messages
        chatter_id_str = f"{chatter_id}"
        unread_messages_list[chatter_id_str] = []
        serializer = BoxSerializer(box, data={"unread_messages": unread_messages_list}, partial=True)
        if serializer.is_valid():
            serializer.save()
