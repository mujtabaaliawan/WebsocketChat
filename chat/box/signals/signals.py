from room.models import Room
from django.db.models.signals import post_save
from django.dispatch import receiver
from box.serializers import BoxSerializer


@receiver(post_save, sender=Room, weak=False)
def create_group_token(sender, instance=None, created=False, **kwargs):
    room = sender.objects.last()
    owner_id = room.owner.id
    if created:
        BoxSerializer(data={'name': 'main', 'room': room, 'chatter': [owner_id], 'is_active': True})
