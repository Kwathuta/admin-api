from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from apps.superadmin.serializers import *
from apps.superadmin.permissions import *

class UserView(APIView):
    """This handles user functionality

    Args:
        generics ([type]): [description]
    """
    schema = get_schema_view()
    permission_classes = [IsAuthenticated & CreateUserPermission]

    @swagger_auto_schema(request_body=UserCreationSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "The account was successfully created"
            responseStatus = status.HTTP_201_CREATED
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            print(data)
            responseStatus = status.HTTP_400_BAD_REQUEST
            return Response(data,status = responseStatus)

class LoginView(APIView):
    """This handles a user login request

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validate_user()
            data['user'] = GetUserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            responseStatus = status.HTTP_200_OK
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            return Response(data,status = status.HTTP_400_BAD_REQUEST)


class RoleView(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsAuthenticated & ChangeRolePermission]

    @swagger_auto_schema(request_body=SetRoleSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = SetRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user's role was successfully updated"
            responseStatus = status.HTTP_200_OK


        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,status = responseStatus)

