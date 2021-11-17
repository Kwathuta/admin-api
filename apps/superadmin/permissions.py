from rest_framework import permissions

from django.contrib.auth.models import Group

class CreateUserPermission(permissions.BasePermission):
    """This determines whether a user is authorized to create users depending on their group

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False