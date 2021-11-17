from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from apps.superadmin.serializers import *
from apps.superadmin.permissions import *

class UserView(APIView):
    """This handles user functionality

    Args:
        generics ([type]): [description]
    """
    permission_classes = [IsAuthenticated & CreateUserPermission]
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

class RoleView(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsAuthenticated & CreateUserPermission]

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

