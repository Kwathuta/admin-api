from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import render

from .serializers import ApproveLeaveSerializer, EmployeeSerializer, CreateEmployeeSerializer, LeaveSerializer, CreateLeaveSerializer, DepartmentSerializer, EmploymentTypeSerializer, BankDetailsSerializer

# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import BankDetails, Employee, Leave, EmploymentType, Department
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
    
    
    
# approve leave using its id
class ApproveLeave(APIView):
    def get_object(self, id):
        try:
            return Leave.objects.get(id=id)
        except Leave.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):  # approve leave
        leave = self.get_object(id)
        serializer = ApproveLeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# list departments
class DepartmentView(APIView):
    def get(self, request, format=None):  # get all departments
        all_departments = Department.objects.all()
        serializers = DepartmentSerializer(all_departments, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create department
        serializers = DepartmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Department created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# list employment types
class EmploymentTypeView(APIView):
    def get(self, request, format=None):  # get all employment types
        all_employment_types = EmploymentType.objects.all()
        serializers = EmploymentTypeSerializer(all_employment_types, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create employment type
        serializers = EmploymentTypeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Employment type created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# bank details
class BankDetailsView(APIView):
    def get(self, request, format=None):  # get all bank details
        all_bank_details = BankDetails.objects.all()
        serializers = BankDetailsSerializer(all_bank_details, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create bank details
        serializers = BankDetailsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Bank details created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
