from rest_framework import fields, serializers
from django.contrib.auth.models import Group

from apps.superadmin.models import *

class GroupSerializer(serializers.ModelSerializer):
    """A serializer for the user groups

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Group
        fields = '__all__'

class UserCreationSerializer(serializers.ModelSerializer):
    """This defines the fields used in creating an employee

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = User
        fields = ['email','username','password','nationality','national_id']

    def save(self):
        """This handles saving a user from the request
        """
        account = User(email = self.validated_data['email'], username = self.validated_data['username'],role = Role.objects.get(name="subordinate_staff"))
        account.set_password(self.validated_data['password'])
        account.save()
        return account

class GetUserSerializer(serializers.ModelSerializer):
    """This defines getting the user instances

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    """This defines working with the user roles table

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Role
        fields = ['pk']

class SetRoleSerializer(serializers.Serializer):
    """This defines the parameters to be used in assigning roles

    Args:
        serializers ([type]): [description]
    """
    user = serializers.CharField(max_length=50)
    role = serializers.CharField(max_length=50)

    def save(self):
        user = (self.validated_data['user'])
        role = (self.validated_data['role'])
        try:
            user = User.objects.get(pk = user)
            role = Role.objects.get(pk = role)

            user.role = role
            user.save()

        except Exception as e:
            raise serializers.ValidationError(e)