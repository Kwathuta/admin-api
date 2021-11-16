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
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['email','username','password','nationality','national_id','groups']
