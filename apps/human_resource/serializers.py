from django.db.models import fields
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import fields, serializers


from .models import Employee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter


# department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['pk', 'name']
        
# department serializer
class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['pk', 'name']
        

# leave type serializer
class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['pk', 'name']

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
    # leave_type = serializers.CharField(source='leave_type.name')
    class Meta:
        model = Leave
        fields = '__all__'


# create leave
class CreateLeaveSerializer(serializers.ModelSerializer):  # create leave
    class Meta:
        model = Leave

        fields = (
            "employee", "leave_type", "leave_date_from", "leave_date_to", "status", "leave_type", "positon", "department", "employment_type")

        def create(self, validated_data):
            leave = Leave.objects.create(**validated_data)
            return leave