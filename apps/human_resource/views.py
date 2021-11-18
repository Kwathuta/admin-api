from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import render

from .serializers import EmployeeSerializer, CreateEmployeeSerializer, LeaveSerializer, CreateLeaveSerializer

# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Employee, Leave
from apps.human_resource import serializers


# list employees
class EmployeeView(APIView):
    def get(self, request, format=None):  # get all employees
        all_employees = Employee.objects.all()
        serializers = EmployeeSerializer(all_employees, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create employee
        serializers = CreateEmployeeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            # data['success'] = "Employee created successfully"
            return Response({"Employee created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# employee details
class EmployeeDetail(APIView):  # get employee details
    def get_object(self, employee_id):
        try:
            return Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, employee_id, format=None):  # get employee details
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, employee_id, format=None):  # update employee details
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id, format=None):
        employee = self.get_object(employee_id)
        employee.delete()
        return Response({"Employee deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


# list leave
class LeaveView(APIView):
    def get(self, request, format=None):  # get all leave
        all_leave = Leave.objects.all()
        serializers = LeaveSerializer(all_leave, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create leave
        serializers = CreateLeaveSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            # data['success'] = "Leave created successfully"
            return Response({"Leave created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
