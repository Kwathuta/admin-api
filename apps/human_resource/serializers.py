from django.db import models
from django.db.models import fields
from rest_framework import fields, serializers, validators
from phonenumber_field.modelfields import PhoneNumberField


from .models import Employee, EmploymentInformation, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter, EmployeeProfile
from apps.superadmin.models import *


# employee profile serializer
class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'

# department serializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


# employeeDetails serializer
class EmployeeDetailsSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    # department_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Department.objects.all())

    profile = EmployeeProfileSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "pk",
            "employee_id",
            "country",
            "date_of_birth",
            "email",
            "other_names",
            "national_id",
            "surname",
            "is_active",
            "department",
            "profile",
        ]
        # exclude = ['password']


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

    department = DepartmentSerializer()
    employee = EmployeeDetailsSerializer()
    employment_type = EmploymentTypeSerializer()

    class Meta:
        model = EmploymentInformation
        fields = '__all__'
        
        



def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
# create employee


class CreateEmployeeSerializer(serializers.Serializer):  # create employee
    department = serializers.IntegerField(validators=[required])
    employment_type = serializers.IntegerField(validators=[required])
    position = serializers.CharField(validators=[required])
    employment_date = serializers.DateField(validators=[required])
    gross_salary = serializers.DecimalField(
        max_digits=10, decimal_places=2, validators=[required])
    marital_status = serializers.ChoiceField(
        choices=marital_choices, validators=[required])
    emergency_contact = serializers.CharField(validators=[required])
    emergency_contact_number = serializers.CharField(validators=[required])
    bank_name = serializers.CharField(validators=[required])
    bank_branch = serializers.CharField(validators=[required])
    account_number = serializers.CharField(validators=[required])
    phone_number = serializers.CharField(validators=[required], max_length=10)
    surname = serializers.CharField(validators=[required])
    employee_id = serializers.CharField(validators=[required])
    date_of_birth = serializers.DateField(validators=[required])
    country = serializers.CharField(validators=[required])
    email = serializers.EmailField(validators=[required])
    other_names = serializers.CharField(validators=[required])
    national_id = serializers.CharField(validators=[required])
    password = serializers.CharField(validators=[required])

    def save(self):
        try:
            department = Department.objects.get(
                pk=self.validated_data['department'])
            employment_type = EmploymentType.objects.get(
                pk=self.validated_data['employment_type'])
        except:
            raise serializers.ValidationError(
                "Some of the specified fields from your request were not found")

        employee = Employee(surname=self.validated_data['surname'], other_names=self.validated_data['other_names'], email=self.validated_data['email'], national_id=self.validated_data[
                            'national_id'], date_of_birth=self.validated_data['date_of_birth'], country=self.validated_data['country'], role=Role.objects.get(name="subordinate_staff"))
        employee.set_password(self.validated_data['password'])
        employee.save()

        employee_profile = EmployeeProfile.objects.get(employee=employee)
        employee_profile.marital_status = self.validated_data['marital_status']
        employee_profile.phone_number = self.validated_data['phone_number']
        employee_profile.save()

        # PaymentInformation(employee = employee,bank_name = self.validated_data['bank_name'],branch = self.validated_data['bank_branch'],account_number = self.validated_data['account_number'],gross_pay = self.validated_data['gross_salary']).save()
        employee_payment = PaymentInformation.objects.get(employee=employee)
        employee_payment.bank_name = self.validated_data['bank_name']
        employee_payment.branch = self.validated_data['bank_branch']
        employee_payment.account_number = self.validated_data['account_number']
        employee_payment.gross_pay = self.validated_data['gross_salary']
        employee_payment.save()

        # EmergencyInformation(employee = employee,name = self.validated_data['emergency_contact'],phone_number = self.validated_data['emergency_contact_number']).save()
        employee_emergency = EmergencyInformation.objects.get(
            employee=employee)
        employee_emergency.name = self.validated_data['emergency_contact']
        employee_emergency.phone_number = self.validated_data['emergency_contact_number']
        employee_emergency.save()

        # EmploymentInformation(employee = employee,position = self.validated_data['position'],department = department,employment_type = employment_type).save()
        employee_employment = EmploymentInformation.objects.get(
            employee=employee)
        employee_employment.position = self.validated_data['position']
        employee_employment.department = department
        employee_employment.employment_type = employment_type
        employee_employment.save()

        return employee


# leave serializer
class LeaveSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    employment_type = serializers.CharField(source='employment_type.name')
    leave_type = serializers.CharField(source='leave_type.name')
    employee = serializers.CharField(source='employee.other_names')
    approved_by = serializers.CharField(source='employee.surname')

    class Meta:
        model = Leave
        fields = '__all__'


# create leave
class CreateLeaveSerializer(serializers.ModelSerializer):  # create leave
    # employee = serializers.CharField(source='employee.other_names')
    # leave_type = serializers.CharField(source='leave_type.name')
    # department = serializers.CharField(source='department.name')
    # employment_type = serializers.CharField(source='employment_type.name')

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
        
        # update status in EmploymentInformation to False
        # def update_employment_status(self, instance, validated_data):
        #     instance.status = validated_data.get('status', instance.status)
        #     instance.save()
        #     return instance


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
