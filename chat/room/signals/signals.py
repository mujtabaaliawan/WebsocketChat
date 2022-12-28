# from room.models import Room
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from box.serializers import BoxSerializer
#
#
# @receiver(post_save, sender=Room, weak=False)
# def create_main_box(sender, instance=None, created=False, **kwargs):
#     room = sender.objects.last()
#     owner_id = room.owner.id
#
#     if created:
#         serializer = BoxSerializer(data={"name": "main",
#                                    "room_id": room.id, "is_active": "True"})
#         serializer.is_valid()
#         box = serializer.save()
#         box.chatter.add(owner_id)
