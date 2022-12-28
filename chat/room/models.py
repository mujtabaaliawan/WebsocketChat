from django.db import models
from chatter.models import Chatter


class Room(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(Chatter, on_delete=models.CASCADE)
