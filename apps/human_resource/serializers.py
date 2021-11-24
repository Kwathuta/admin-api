from django.db import models
from django.db.models import fields
from rest_framework import fields, serializers, validators
from phonenumber_field.modelfields import PhoneNumberField


from .models import Employee, EmploymentInformation, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter
from apps.superadmin.models import *

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


# # create employee
# class CreateEmployeeSerializer(serializers.ModelSerializer):  # create employee
#     class Meta:
#         model = Employee
#         fields = (
#             'employee_id', 'department', 'employment_type', 'surname',
#             'other_names', 'phone_number', 'work_email', 'id_number',
#             'country', 'date_of_birth', 'position', 'department',
#             'employment_type', 'employment_date', 'gross_salary',
#             'marital_status', 'emergency_contact', 'emergency_contact_number',
#             'bank_payment_details'
#         )

#         # create employee

#         def create(self, validated_data):
#             employee = Employee.objects.create(**validated_data)
#             return employee

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
# create employee
class CreateEmployeeSerializer(serializers.Serializer):  # create employee
    department = serializers.IntegerField(validators=[required])
    employment_type = serializers.IntegerField(validators=[required])
    position = serializers.CharField(validators=[required])
    employment_date = serializers.DateField(validators=[required])
    gross_salary = serializers.DecimalField(max_digits=10,decimal_places=2,validators=[required])
    marital_status = serializers.ChoiceField(choices=marital_choices,validators=[required])
    emergency_contact = serializers.CharField(validators=[required])
    emergency_contact_number = serializers.CharField(validators=[required])
    bank_name = serializers.CharField(validators=[required])
    bank_branch = serializers.CharField(validators=[required])
    account_number = serializers.CharField(validators=[required])
    phone_number = serializers.CharField(validators=[required],max_length=10)
    surname = serializers.CharField(validators=[required])
    employee_id =  serializers.CharField(validators=[required])
    date_of_birth = serializers.DateField(validators=[required])
    country = serializers.CharField(validators=[required])
    email = serializers.EmailField(validators=[required])
    other_names = serializers.CharField(validators=[required])
    national_id = serializers.CharField(validators=[required])
    password = serializers.CharField(validators=[required])
    
    # class Meta:
    # fields = (
    #     'employee_id', 'department', 'employment_type', 'surname',
    #     'other_names', 'phone_number', 'email', 'national_id',
    #     'country', 'date_of_birth', 'position','employment_date', 'gross_salary',
    #     'marital_status', 'emergency_contact', 'emergency_contact_number',
    #     'bank_name','bank_branch','account_number'
    # )

    # create employee

    def save(self):
        try:
            department = Department.objects.get(pk=self.validated_data['department'])
            employment_type = EmploymentType.objects.get(pk=self.validated_data['employment_type'])
        except:
            raise serializers.ValidationError("Some of the specified fields from your request were not found")

        employee = Employee(surname=self.validated_data['surname'],other_names=self.validated_data['other_names'],email = self.validated_data['email'],national_id = self.validated_data['national_id'],date_of_birth = self.validated_data['date_of_birth'],country = self.validated_data['country'],role = Role.objects.get(name="subordinate_staff"))
        employee.set_password(self.validated_data['password'])
        employee.save()

        employee_profile = EmployeeProfile.objects.get(employee=employee)
        employee_profile.marital_status = self.validated_data['marital_status']
        employee_profile.phone_number = self.validated_data['phone_number']
        employee_profile.save()

        PaymentInformation(employee = employee,bank_name = self.validated_data['bank_name'],branch = self.validated_data['bank_branch'],account_number = self.validated_data['account_number'],gross_pay = self.validated_data['gross_salary']).save()
        EmergencyInformation(employee = employee,name = self.validated_data['emergency_contact'],phone_number = self.validated_data['emergency_contact_number']).save()
        EmploymentInformation(employee = employee,position = self.validated_data['position'],department = department,employment_type = employment_type).save()

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


# create application
class CreateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'      
        
        # create application
        def create(self, validated_data):
            application = Application.objects.create(**validated_data)
            return application

# view application
class ApplicationSerializer(serializers.ModelSerializer):
    job_listing = serializers.CharField(source='job_listing.job_title')
    class Meta:
        model = Application
        fields = '__all__'