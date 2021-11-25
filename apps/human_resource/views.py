from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import render

from .serializers import ApplicationSerializer, ApplicationStatusSerializer, CreateScheduleInterviewSerializer, EmployeeDetailsSerializer, JobListingSerializer, ApproveLeaveSerializer, EmployeeSerializer, CreateEmployeeSerializer, LeaveSerializer, CreateLeaveSerializer, DepartmentSerializer, EmploymentTypeSerializer, CreateJobListingSerializer, CreateApplicationSerializer, ScheduledInterviewSerializer

# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from .models import Application, Employee, EmploymentInformation, JobListing, Leave, EmploymentType, Department, ScheduledInterview
from apps.human_resource import serializers

from django.core.mail import send_mail


# list employees
class EmployeeView(APIView):
    def get(self, request, format=None):  # get all employees
        all_employees = EmploymentInformation.objects.all()
        serializers = EmployeeSerializer(all_employees, many=True)
        return Response(serializers.data)


# employee details
class EmployeeDetail(APIView):  # get employee details
    def get_object(self, id):
        try:
            return EmploymentInformation.objects.get(id=id)
        except EmploymentInformation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):  # get employee details
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    # @swagger_auto_schema(request_body=EmployeeSerializer)
    def put(self, request, id, format=None):  # update employee details
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        employee = self.get_object(id)
        employee.delete()
        return Response({"Employee deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


# list leave
class LeaveView(APIView):
    def get(self, request, format=None):  # get all leave
        all_leave = Leave.get_all_pending_leaves()
        serializers = LeaveSerializer(all_leave, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(request_body=CreateLeaveSerializer)
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


# onleave employee list
class OnLeaveEmployees(APIView):
    def get(self, request, format=None):  # get all onleave employees
        all_employees = Leave.get_all_approved_leaves_and_active()
        serializers = LeaveSerializer(all_employees, many=True)
        return Response(serializers.data)


# active employee list
class ActiveEmployees(APIView):
    def get(self, request, format=None):  # get all employees
        all_employees = EmploymentInformation.get_all_active_employees()
        serializers = EmployeeSerializer(all_employees, many=True)
        return Response(serializers.data)


# list departments
class DepartmentView(APIView):
    def get(self, request, format=None):  # get all departments
        all_departments = Department.objects.all()
        serializers = DepartmentSerializer(all_departments, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(request_body=DepartmentSerializer)
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

    @swagger_auto_schema(request_body=EmploymentTypeSerializer)
    def post(self, request, format=None):  # create employment type
        serializers = EmploymentTypeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Employment type created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# create job listing
class JobListingView(APIView):
    def get(self, request, format=None):  # get all job listings
        all_job_listings = JobListing.objects.all()
        serializers = JobListingSerializer(all_job_listings, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(request_body=CreateJobListingSerializer)
    def post(self, request, format=None):
        serializers = CreateJobListingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Job listing created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# get active job listings
class ActiveJobListingView(APIView):
    def get(self, request, format=None):  # get all active job listings
        all_job_listings = JobListing.get_active_job_listing()
        serializers = JobListingSerializer(all_job_listings, many=True)
        return Response(serializers.data)


# get past job listings
class PastJobListingView(APIView):
    def get(self, request, format=None):  # get all past job listings
        all_job_listings = JobListing.get_past_job_listing()
        serializers = JobListingSerializer(all_job_listings, many=True)
        return Response(serializers.data)


# create application
class ApplicationView(APIView):
    def get(self, request, format=None):  # get all applications
        all_applications = Application.objects.all()
        serializers = ApplicationSerializer(all_applications, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(request_body=CreateApplicationSerializer)
    def post(self, request, format=None):
        serializers = CreateApplicationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Application created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# get new applications
class NewApplicationView(APIView):
    def get(self, request, format=None):  # get all new applications
        all_applications = Application.get_new_application()
        serializers = ApplicationSerializer(all_applications, many=True)
        return Response(serializers.data)


# get past applications
class PastApplicationView(APIView):
    def get(self, request, format=None):  # get all past applications
        all_applications = Application.get_past_applications()
        serializers = ApplicationSerializer(all_applications, many=True)
        return Response(serializers.data)


#  get a spacific particular application
class ApplicationDetail(APIView):
    def get_object(self, id):
        try:
            return Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        application = self.get_object(id)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        application = self.get_object(id)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update application status
class ApplicationStatusView(APIView):
    def get_object(self, id):
        try:
            return Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Http404
    @swagger_auto_schema(request_body=ApplicationStatusSerializer)
    def put(self, request, id, format=None):
        application = self.get_object(id)
        serializers = ApplicationStatusSerializer(
            application, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"Application status updated successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# create schedule interview
class InterviewView(APIView):
    def get(self, request, format=None):  # get all schedule interviews
        all_schedule_interviews = ScheduledInterview.get_all_scheduled_interviews()
        serializers = ScheduledInterviewSerializer(
            all_schedule_interviews, many=True)
        return Response(serializers.data)


# create interview
class ScheduleInterviewView(APIView):
    @swagger_auto_schema(request_body=CreateScheduleInterviewSerializer)
    def post(self, request, format=None):  # create schedule interview
        serializers = CreateScheduleInterviewSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()

            # get the email of the applicant and send an email to the applicant to notify them of the interview
            applicant_email = request.data['email']
            interview_time_from = serializers.data['interview_time_from']
            interview_time_to = serializers.data['interview_time_to']
            interview_date = serializers.data['interview_date']
            content = 'Hello,\n\nYou have an interview scheduled for ' + interview_date + ' from ' + interview_time_from + \
                ' to ' + interview_time_to + '.\n\n' + \
                serializers.data['content'] + \
                '.\n\nRegards,\n\nFuzuPay Hiring Team'
            subject = 'Interview Scheduled - FuzuPay'

            send_mail(subject, content, 'hiring@fuzupay.com',
                      [applicant_email], fail_silently=False)
            return Response({"Scheduled interview sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
