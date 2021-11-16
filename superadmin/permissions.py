from rest_framework import permissions

from django.contrib.auth.models import Group

class CreateUserPermission(permissions.BasePermission):
    """This determines whether a user is authorized to create users depending on their group

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name="humanresource").exists():
            print("not working")
            return True
        else:
            print("working")
            return False