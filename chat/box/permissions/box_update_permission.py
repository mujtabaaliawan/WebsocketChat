from rest_framework.permissions import BasePermission
from box.models import Box


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        box_owner = Box.objects.get(id=pk).owner
        return request.user.id == box_owner.user_id
