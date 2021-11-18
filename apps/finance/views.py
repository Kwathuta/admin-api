from django.shortcuts import render
from django.http import JsonResponse
from .models import Approve
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ApproveSerializer

# Create your views here.
class ApproveDetail(APIView):  # get, update, delete single employee
   
    def get_object(self, pk):
        try:
            return Approve.objects.get(pk=pk)
        except Approve.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):  # get employee
        notes = self.get_object(pk)
        serializers = ApproveSerializer(notes)
        return Response(serializers.data)

    def put(self, request, pk, format=None):  # update employee
        notes = self.get_object(pk)
        serializers = ApproveSerializer(notes, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # delete employee
        notes = self.get_object(pk)
        notes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApproveList(APIView):  # get all employee
   

    def get(self, request, format=None):  # get all employee
        all_notes = Approve.objects.all()
        serializers = ApproveSerializer(all_notes, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create new employee
        serializers = ApproveSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
