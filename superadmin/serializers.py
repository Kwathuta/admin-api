from rest_framework import fields, serializers
from django.contrib.auth.models import Group

from superadmin.models import *

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
    groups = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email','username','password','nationality','national_id','groups']

    def save(self):
        """This handles saving a user from the request
        """
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(self.validated_data['password'])

        group = Group.objects.get(pk=int(self.validated_data['groups']))

        account.save()
        account.groups.add(group)
        account.save()
        return account
