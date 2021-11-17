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
