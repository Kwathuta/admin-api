from django.db.models import fields
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import fields, serializers


from .models import Employee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter


# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


# create employee
class CreateEmployeeSerializer(serializers.ModelSerializer):  # create employee
    class Meta:
        model = Employee
        fields = (
            'department', 'employment_type', 'surname',
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
