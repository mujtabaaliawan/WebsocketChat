from django.db import models
from chatter.models import Chatter
from box.models import Box


class Message(models.Model):

    message = models.CharField(max_length=255)
    box = models.ForeignKey(Box, on_delete=models.PROTECT, related_name='message_box')
    sender = models.ForeignKey(Chatter, on_delete=models.PROTECT, related_name='message_sender')
    creation_time = models.DateTimeField(auto_now_add=True)
