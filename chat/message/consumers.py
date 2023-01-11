# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from box.models import Box
from message.models import Message
from message.serializers import MessageSerializer
from chatter.models import Chatter
from box.serializers import BoxSerializer
import datetime


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        user = self.scope["user"]
        box_id = self.scope["url_route"]["kwargs"]["box_id"]
        self.room_group_name = "chat_%s" % box_id
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.update_box_detail_enter(user, box_id)

    def disconnect(self, close_code):
        # Leave room group
        user = self.scope["user"]
        box_id = self.scope["url_route"]["kwargs"]["box_id"]

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.update_box_detail_exit(user, box_id)

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

    def update_box_detail_enter(self, user, box_id):
        chatter = Chatter.objects.get(user_id=user.id)
        chatter_id = chatter.id
        chatter_id_str = f"{chatter_id}"
        box = Box.objects.get(id=box_id)
        old_box_detail = box.box_detail

        old_box_detail.setdefault("online_chatters", [])
        old_box_detail["online_chatters"].append(chatter_id)

        old_box_detail.setdefault("users_sessions_details", {})
        old_box_detail.setdefault("last_session_details", {})
        old_box_detail["users_sessions_details"].setdefault(chatter_id_str, {})
        old_box_detail["last_session_details"].setdefault(chatter_id_str, {})

        old_box_detail.setdefault("highest_average_session_duration", "00:00:00")
        old_box_detail.setdefault("highest_average_session_duration_chatter_id", 0)
        old_box_detail.setdefault("lowest_average_session_duration", "23:59:59")
        old_box_detail.setdefault("lowest_average_session_duration_chatter_id", 0)
        old_box_detail.setdefault("highest_session_duration", "00:00:00")
        old_box_detail.setdefault("highest_session_duration_chatter_id", 0)
        old_box_detail.setdefault("lowest_session_duration", "23:59:59")
        old_box_detail.setdefault("lowest_session_duration_chatter_id", 0)

        old_box_detail["users_sessions_details"][chatter_id_str].setdefault("average_session_duration", "00:00:00")

        old_box_detail["users_sessions_details"][chatter_id_str].setdefault("session", {})

        sessions_list = list(old_box_detail["users_sessions_details"][chatter_id_str]["session"])
        if len(sessions_list) > 0:
            last_session = sessions_list[-1]
        else:
            last_session = 0

        previous_session_number = int(last_session)
        new_session_number = previous_session_number + 1
        new_session_number_str = str(new_session_number)
        old_box_detail["users_sessions_details"][chatter_id_str]["session"].setdefault(new_session_number_str, {})
        login_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        old_box_detail["users_sessions_details"][chatter_id_str]["session"][new_session_number_str].setdefault(
            "login_time", login_time)
        old_box_detail["last_session_details"][chatter_id_str]["login_time"] = login_time

        serializer = BoxSerializer(box, data={"box_detail": old_box_detail}, partial=True)
        if serializer.is_valid():
            serializer.save()

    def update_box_detail_exit(self, user, box_id):
        chatter = Chatter.objects.get(user_id=user.id)
        chatter_id = chatter.id
        chatter_id_str = f"{chatter_id}"
        box = Box.objects.get(id=box_id)
        old_box_detail = box.box_detail

        old_box_detail["online_chatters"].remove(chatter_id)

        new_session_number_str = list(old_box_detail["users_sessions_details"][chatter_id_str]["session"])[-1]

        logout_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        old_box_detail["users_sessions_details"][chatter_id_str]["session"][new_session_number_str].setdefault(
            "logout_time", logout_time)
        old_box_detail["last_session_details"][chatter_id_str]["logout_time"] = logout_time

        # session_duration
        login_time = datetime.datetime.strptime(
            old_box_detail["users_sessions_details"][chatter_id_str]["session"][new_session_number_str][
                "login_time"], '%d/%m/%Y %H:%M:%S')
        logout_time = datetime.datetime.strptime(
            old_box_detail["users_sessions_details"][chatter_id_str]["session"][new_session_number_str][
                "logout_time"], '%d/%m/%Y %H:%M:%S')
        duration = logout_time - login_time
        duration_str = str(duration)
        old_box_detail["users_sessions_details"][chatter_id_str]["session"][new_session_number_str].setdefault(
            "duration", duration_str)
        old_box_detail["last_session_details"][chatter_id_str]["duration"] = duration_str

        # highest_duration
        duration_seconds = self.convert_time_string_to_total_seconds(duration_str)

        highest_session_duration_seconds = self.convert_time_string_to_total_seconds(
            old_box_detail["highest_session_duration"])
        if duration_seconds > highest_session_duration_seconds:
            old_box_detail["highest_session_duration"] = duration_str
            old_box_detail["highest_session_duration_chatter_id"] = chatter_id_str

        # lowest_duration
        lowest_session_duration_seconds = self.convert_time_string_to_total_seconds(
            old_box_detail["lowest_session_duration"])
        if duration_seconds < lowest_session_duration_seconds:
            old_box_detail["lowest_session_duration"] = duration_str
            old_box_detail["lowest_session_duration_chatter_id"] = chatter_id_str

        # average_session_duration
        previous_average_duration = old_box_detail["users_sessions_details"][chatter_id_str]["average_session_duration"]
        old_average_duration_seconds = self.convert_time_string_to_total_seconds(time_string=previous_average_duration)
        old_session_number = int(new_session_number_str) - 1
        total_sum = (old_average_duration_seconds * old_session_number) + self.convert_time_string_to_total_seconds(
            duration_str)
        new_average_session_duration_seconds = float(total_sum / int(new_session_number_str))
        new_average_session_duration_str = str(datetime.timedelta(seconds=new_average_session_duration_seconds))
        old_box_detail["users_sessions_details"][chatter_id_str]["average_session_duration"] =\
            new_average_session_duration_str

        # highest_average_session_duration
        highest_average_session_duration = old_box_detail["highest_average_session_duration"]
        if old_box_detail["highest_average_session_duration_chatter_id"] == chatter_id_str:
            self.find_new_highest_average_duration(old_box_detail)
        elif new_average_session_duration_seconds > self.convert_time_string_to_total_seconds(
                highest_average_session_duration):
            old_box_detail["highest_average_session_duration"] = new_average_session_duration_str
            old_box_detail["highest_average_session_duration_chatter_id"] = chatter_id_str

        # lowest_average_session_duration
        lowest_average_session_duration = old_box_detail["lowest_average_session_duration"]
        if old_box_detail["lowest_average_session_duration_chatter_id"] == chatter_id_str:
            self.find_new_lowest_average_duration(old_box_detail)
        elif new_average_session_duration_seconds < self.convert_time_string_to_total_seconds(
                lowest_average_session_duration):
            old_box_detail["lowest_average_session_duration"] = new_average_session_duration_str
            old_box_detail["lowest_average_session_duration_chatter_id"] = chatter_id_str

        print(old_box_detail)
        serializer = BoxSerializer(box, data={"box_detail": old_box_detail}, partial=True)
        if serializer.is_valid():
            serializer.save()

    def convert_time_string_to_total_seconds(self, time_string):
        hours, minutes, seconds = time_string.split(':')
        total_seconds = (int(hours) * 3600) * (int(minutes) * 60) + float(seconds)
        return total_seconds

    def find_new_highest_average_duration(self, old_box_detail):
        highest_average_session_duration = "00:00:00"
        highest_average_session_duration_chatter_id = '0'
        for chatters in old_box_detail["users_sessions_details"]:
            average_session_duration = self.convert_time_string_to_total_seconds(
                old_box_detail["users_sessions_details"][chatters]["average_session_duration"])
            highest_average_session_duration = self.convert_time_string_to_total_seconds(
                highest_average_session_duration)

            if average_session_duration > highest_average_session_duration:
                highest_average_session_duration = old_box_detail["users_sessions_details"][chatters][
                    "average_session_duration"]
                highest_average_session_duration_chatter_id = chatters

        old_box_detail["highest_average_session_duration"] = highest_average_session_duration
        old_box_detail["highest_average_session_duration_chatter_id"] = highest_average_session_duration_chatter_id

    def find_new_lowest_average_duration(self, old_box_detail):
        lowest_average_session_duration = "23:59:59"
        lowest_average_session_duration_chatter_id = '0'

        for chatters in old_box_detail["users_sessions_details"]:

            average_session_duration = self.convert_time_string_to_total_seconds(
                old_box_detail["users_sessions_details"][chatters]["average_session_duration"])
            lowest_average_session_duration = self.convert_time_string_to_total_seconds(
                lowest_average_session_duration)

            if average_session_duration < lowest_average_session_duration:
                lowest_average_session_duration = old_box_detail["users_sessions_details"][chatters][
                    "average_session_duration"]
                lowest_average_session_duration_chatter_id = chatters

        old_box_detail["lowest_average_session_duration"] = lowest_average_session_duration
        old_box_detail["lowest_average_session_duration_chatter_id"] = lowest_average_session_duration_chatter_id
