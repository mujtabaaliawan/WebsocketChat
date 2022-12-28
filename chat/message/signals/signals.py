# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from message.models import Message
#
#
# @receiver(post_save, sender=Message, weak=False)
# def populate_msg_send_list(sender, instance=None, created=False, **kwargs):
#     message = sender.objects.last()
#     box = message.box
#     box_chatters = box.chatter
#     msg_list = box.room.unread_messages
#     if created:
#         for chatter in box_chatters.objects.all():
#             chatter_id = str(chatter.id)
#             new_message_id = message.id
#             check_chatter = msg_list.get(chatter_id, value=0)
#             if check_chatter == 0:
#                 msg_list.update({chatter_id: [new_message_id]})
#                 continue
#             msgs_to_send = msg_list.get(chatter_id)
#             new_msgs_to_send = msgs_to_send.append(new_message_id)
#             msg_list.update({chatter_id: new_msgs_to_send})

