from django.db import models
from django.db.models import fields
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import fields, serializers


from .models import Employee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter


# department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

# department serializer


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['id', 'name']

# bank details serializer


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ['id', 'account_number', 'bank_name', 'branch_name']

# leave type serializer


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name']

# Employee Serializer


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    employment_type = serializers.CharField(source='employment_type.name')

    class Meta:
        model = Employee
        fields = '__all__'


# create employee
class CreateEmployeeSerializer(serializers.ModelSerializer):  # create employee
    class Meta:
        model = Employee
        fields = (
            'employee_id', 'department', 'employment_type', 'surname',
            'other_names', 'phone_number', 'work_email', 'id_number',
            'country', 'date_of_birth', 'position', 'department',
            'employment_type', 'employment_date', 'gross_salary',
            'marital_status', 'emergency_contact', 'emergency_contact_number',
            'bank_payment_details'
        )

        # create employee

        def create(self, validated_data):
            employee = Employee.objects.create(**validated_data)
            return employee


# leave serializer
class LeaveSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    employment_type = serializers.CharField(source='employment_type.name')
    leave_type = serializers.CharField(source='leave_type.name')
    employee = serializers.CharField(source='employee.other_names')
    approved_by = serializers.CharField(source='user.username')

    class Meta:
        model = Leave
        fields = '__all__'


# create leave
class CreateLeaveSerializer(serializers.ModelSerializer):  # create leave
    employee = serializers.CharField(source='employee.other_names')
    leave_type = serializers.CharField(source='leave_type.name')
    department = serializers.CharField(source='department.name')
    employment_type = serializers.CharField(source='employment_type.name')

    class Meta:
        model = Leave

        fields = (
            "employee", "leave_type", "leave_date_from", "leave_date_to", "status", "leave_type", "positon", "department", "employment_type")

        def create(self, validated_data):
            leave = Leave.objects.create(**validated_data)
            return leave


# approve leave
class ApproveLeaveSerializer(serializers.ModelSerializer):  # approve leave
    class Meta:
        model = Leave
        fields = ('pk', 'status')

        def update(self, instance, validated_data):
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance


# job listing serializer
class JobListingSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    class Meta:
        model = JobListing
        fields = '__all__'


# create job listing
class CreateJobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = (
            'job_title',
            'job_description',
            'department',
            'position',
            'location',
            'job_type',
            'experience',
            'salary',
            'deadline'
        )

        def create(self, validated_data):
            job_listing = JobListing.objects.create(**validated_data)
            return job_listing
