from django.db.models import fields
from rest_flex_fields import FlexFieldsModelSerializer


from .models import Employee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter


# Employee Serializer
class EmployeeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


# create employee
class CreateEmployeeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = ( 'employee_id', )