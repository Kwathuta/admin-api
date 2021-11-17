from rest_framework import permissions

from django.contrib.auth.models import Group

class CreateUserPermission(permissions.BasePermission):
    """This determines whether a user is authorized to create users depending on their group

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        print(request.user.role.name)
        if request.user.role.name=="super_admin" or request.user.role.name=="human_resources":
            return True
        else:
            return False
