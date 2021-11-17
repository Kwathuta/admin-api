from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import render

from .serializers import EmployeeSerializer

# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Employee
from apps.human_resource import serializers


# list employees
class EmployeeViewSet(APIView):
    def get(self, request, format=None):  # get all employees
        all_employees = Employee.objects.all()
        serializers = EmployeeSerializer(all_employees, many=True)
        return Response(serializers.data)
    
    # def post(self, request, format=None):
        
