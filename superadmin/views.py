from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from superadmin.serializers import *

class UserView(APIView):
    """This handles user functionality

    Args:
        generics ([type]): [description]
    """
    permission_classes = [IsAuthenticated]
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