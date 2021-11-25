from rest_framework import fields, serializers
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

from apps.superadmin.models import *
from apps.human_resource.models import *

class GroupSerializer(serializers.ModelSerializer):
    """A serializer for the user groups

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Group
        fields = '__all__'

# class UserCreationSerializer(serializers.ModelSerializer):
#     """This defines the fields used in creating an employee

#     Args:
#         serializers ([type]): [description]
#     """
#     class Meta:
#         model = User
#         fields = ['email','username','password','nationality','national_id']

#     def save(self):
#         """This handles saving a user from the request
#         """
#         account = User(email = self.validated_data['email'], username = self.validated_data['username'],role = Role.objects.get(name="subordinate_staff"))
#         account.set_password(self.validated_data['password'])
#         account.save()
#         return account

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

        # PaymentInformation(employee = employee,bank_name = self.validated_data['bank_name'],branch = self.validated_data['bank_branch'],account_number = self.validated_data['account_number'],gross_pay = self.validated_data['gross_salary']).save()
        employee_payment = PaymentInformation.objects.get(employee = employee)
        employee_payment.bank_name = self.validated_data['bank_name']
        employee_payment.branch = self.validated_data['bank_branch']
        employee_payment.account_number = self.validated_data['account_number']
        employee_payment.gross_pay = self.validated_data['gross_salary']
        employee_payment.save()

        # EmergencyInformation(employee = employee,name = self.validated_data['emergency_contact'],phone_number = self.validated_data['emergency_contact_number']).save()
        employee_emergency = EmergencyInformation.objects.get(employee = employee)
        employee_emergency.name = self.validated_data['emergency_contact']
        employee_emergency.phone_number = self.validated_data['emergency_contact_number']
        employee_emergency.save()

        # EmploymentInformation(employee = employee,position = self.validated_data['position'],department = department,employment_type = employment_type).save()
        employee_employment = EmploymentInformation.objects.get(employee = employee)
        employee_employment.position = self.validated_data['position']
        employee_employment.department = department
        employee_employment.employment_type = employment_type
        employee_employment.save()

        return employee

class RoleSerializer(serializers.ModelSerializer):
    """This defines working with the user roles table

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['name']

class GetUserSerializer(serializers.ModelSerializer):
    """This defines getting the user instances

    Args:
        serializers ([type]): [description]

    Parameters: username,password
    """
    role = RoleSerializer()
    class Meta:
        model = Employee
        fields = ['pk','email','surname','other_names','country','national_id','role','date_of_birth']

class LoginSerializer(serializers.Serializer):
    """This defines the functions in the login function

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate_user(self):
        """This handles the validation of the user

        Raises:
            serializers.ValidationError: [description]
        """
        user = authenticate(email = self.validated_data['email'],password = self.validated_data['password'])

        if user is not None:
            return user

        else:
            raise serializers.ValidationError('The user could not be validated with the provided credentials.')

class SetRoleSerializer(serializers.Serializer):
    """This defines the parameters to be used in assigning roles

    Args:
        serializers ([type]): [description]
    """
    user = serializers.CharField(max_length=50)
    role = serializers.CharField(max_length=50)

    def save(self):
        user = (self.validated_data['user'])
        role = (self.validated_data['role'])
        try:
            user = Employee.objects.get(pk = user)
            role = Role.objects.get(pk = role)

            user.role = role
            user.save()

        except Exception as e:
            raise serializers.ValidationError(e)