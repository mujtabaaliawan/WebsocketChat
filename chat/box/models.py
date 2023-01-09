from django.db import models
from chatter.models import Chatter
from room.models import Room


class Box(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Chatter, on_delete=models.PROTECT, related_name='box_owner')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='box_room')
    chatter = models.ManyToManyField(Chatter, blank=True)
    unread_messages = models.JSONField(blank=True, default=dict)
    is_active = models.BooleanField(default=True)
    box_detail = models.JSONField(blank=True, default=dict)

