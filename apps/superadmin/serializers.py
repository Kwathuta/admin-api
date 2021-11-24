from rest_framework import fields, serializers
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

from apps.superadmin.models import *

class GroupSerializer(serializers.ModelSerializer):
    """A serializer for the user groups

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Group
        fields = '__all__'

# class UserCreationSerializer(serializers.ModelSerializer):
#     """This defines the fields used in creating an employee

#     Args:
#         serializers ([type]): [description]
#     """
#     class Meta:
#         model = User
#         fields = ['email','username','password','nationality','national_id']

#     def save(self):
#         """This handles saving a user from the request
#         """
#         account = User(email = self.validated_data['email'], username = self.validated_data['username'],role = Role.objects.get(name="subordinate_staff"))
#         account.set_password(self.validated_data['password'])
#         account.save()
#         return account

class RoleSerializer(serializers.ModelSerializer):
    """This defines working with the user roles table

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['name']

class GetUserSerializer(serializers.ModelSerializer):
    """This defines getting the user instances

    Args:
        serializers ([type]): [description]

    Parameters: username,password
    """
    role = RoleSerializer()
    class Meta:
        model = Employee
        fields = ['pk','email','surname','other_names','country','national_id','role','date_of_birth']

class LoginSerializer(serializers.Serializer):
    """This defines the functions in the login function

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate_user(self):
        """This handles the validation of the user

        Raises:
            serializers.ValidationError: [description]
        """
        user = authenticate(email = self.validated_data['email'],password = self.validated_data['password'])

        if user is not None:
            return user

        else:
            raise serializers.ValidationError('The user could not be validated with the provided credentials.')

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
            user = Employee.objects.get(pk = user)
            role = Role.objects.get(pk = role)

            user.role = role
            user.save()

        except Exception as e:
            raise serializers.ValidationError(e)