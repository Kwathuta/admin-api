from rest_framework import permissions

from django.contrib.auth.models import Group

class CreateUserPermission(permissions.BasePermission):
    """This determines whether a user is authorized to create users depending on their group

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name=="super_admin" or request.user.role.name=="human_resources":
            return True
        else:
            return False

class ChangeRolePermission(permissions.BasePermission):
    """This defines the user with the permission to change another user's role

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        print(view.request.data['user'])
        if request.user.role.name == "super_admin":
            if request.user.pk == int(view.request.data['user']):
                return False
            else:
                return True
        else:
            return False