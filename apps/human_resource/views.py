from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import render

from .serializers import ApplicationSerializer, JobListingSerializer, ApproveLeaveSerializer, EmployeeSerializer, CreateEmployeeSerializer, LeaveSerializer, CreateLeaveSerializer, DepartmentSerializer, EmploymentTypeSerializer, BankDetailsSerializer, CreateJobListingSerializer, CreateApplicationSerializer

# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from .models import Application, BankDetails, Employee, JobListing, Leave, EmploymentType, Department
from apps.human_resource import serializers


# list employees
class EmployeeView(APIView):
    def get(self, request, format=None):  # get all employees
        all_employees = Employee.objects.all()
        serializers = EmployeeSerializer(all_employees, many=True)
        return Response(serializers.data)

    # @swagger_auto_schema(request_body=CreateEmployeeSerializer)
    # def post(self, request, format=None):  # create employee
    #     serializers = CreateEmployeeSerializer(data=request.data)
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response({"Employee created successfully"}, status=status.HTTP_201_CREATED)
    #     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


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


# create job listing
class JobListingView(APIView):
    def get(self, request, format=None):  # get all job listings
        all_job_listings = JobListing.objects.all()
        serializers = JobListingSerializer(all_job_listings, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = CreateJobListingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Job listing created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




# create application
class ApplicationView(APIView):
    def get(self, request, format=None):  # get all applications
        all_applications = Application.objects.all()
        serializers = ApplicationSerializer(all_applications, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = CreateApplicationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Application created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




#  get a particular application
class ApplicationDetail(APIView):
    def get_object(self, application_id):
        try:
            return Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Http404

    def get(self, request, application_id, format=None):
        application = self.get_object(application_id)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    def put(self, request, application_id, format=None):
        application = self.get_object(application_id)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
