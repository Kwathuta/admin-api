from rest_framework import fields, serializers, validators
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from apps.superadmin.tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives


from apps.superadmin.models import *
from apps.human_resource.models import *
from apps.human_resource.serializers import *

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class CompanyCreationSerializer(serializers.Serializer):
    """This is the serializers handling creation of a new company

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    first_name = serializers.CharField(validators=[required])
    last_name = serializers.CharField(validators=[required])
    company_name = serializers.CharField(validators=[required])
    work_email = serializers.EmailField(validators=[required])
    number_of_staff = serializers.CharField(validators=[required])
    country = serializers.ChoiceField(validators=[required],choices=country_choices)
    password = serializers.CharField(validators=[required])

    def save(self,request):
        """This creates the appropriate models

        Raises:
            serializers.ValidationError: [description]
            serializers.ValidationError: [description]
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """
        company = Company(name = self.validated_data['company_name'],number_of_staff = self.validated_data['number_of_staff'],country = self.validated_data['country'])
        company.save()

        first_super_user = Employee(email = self.validated_data['work_email'],surname = self.validated_data['last_name'],role = Role.objects.get(name="super_admin"))
        first_super_user.set_password(self.validated_data['password'])
        first_super_user.save()
        first_super_user.is_active = False
        first_super_user.other_names = self.validated_data['first_name']
        employment_info = EmploymentInformation.objects.get(employee = first_super_user)
        employment_info.company = company
        employment_info.save()
        first_super_user.save()

        current_site = get_current_site(request)

        context = {
            'user': first_super_user,
                'domain': current_site.domain,
                'uid': first_super_user.pk,
                'token': account_activation_token.make_token(first_super_user)
        }

        # render email text
        email_html_message = render_to_string('email/account_activation_email.html', context)
        email_plaintext_message = render_to_string('email/account_activation_email.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            f"Account activation for {first_super_user.surname}",
            # message:
            email_plaintext_message,
            # from:
            "ken.mbira@student.moringaschool.com",
            # to:
            [first_super_user.email]
        )

        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return company

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
    country = serializers.ChoiceField(validators=[required],choices=country_choices)
    email = serializers.EmailField(validators=[required])
    other_names = serializers.CharField(validators=[required])
    national_id = serializers.CharField(validators=[required])

    def save(self,request):
        try:
            department = Department.objects.get(pk=self.validated_data['department'])
            employment_type = EmploymentType.objects.get(pk=self.validated_data['employment_type'])
        except:
            raise serializers.ValidationError("Some of the specified fields from your request were not found")

        employee = Employee(surname=self.validated_data['surname'],employee_id = self.validated_data['employee_id'],other_names=self.validated_data['other_names'],email = self.validated_data['email'],national_id = self.validated_data['national_id'],date_of_birth = self.validated_data['date_of_birth'],country = self.validated_data['country'],role = Role.objects.get(name="subordinate_staff"))
        employee.set_password(self.validated_data['national_id'])
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
        company = EmploymentInformation.objects.get(employee = request.user).company
        print(company)
        employee_employment.company = company
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

class PaymentInfoSerializer(serializers.ModelSerializer):
    """This returs a user's payment information

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        model = PaymentInformation
        fields = ['bank_name','branch','account_number','gross_pay']

class EmergencyInfoSerializer(serializers.ModelSerializer):
    """This returns data of the emergency info of a user

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        model = EmergencyInformation
        fields = ['name','phone_number','relationship']

# department serializer
class Department_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

# department serializer


class Employment_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['name']

class EmployeeInfo(serializers.ModelSerializer):

    department = Department_Serializer()
    employment_type = Employment_TypeSerializer()

    class Meta:
        model = EmploymentInformation
        fields = '__all__'

class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['personal_email','profile_pic','marital_status','insurance_number','phone_number']

class UserDetailsSerializer(serializers.ModelSerializer):
    """This gets everything about a user

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    role = RoleSerializer()
    emergency_information = EmergencyInfoSerializer(read_only=True)
    payment_information = PaymentInfoSerializer(read_only=True)
    employmentinformation = EmployeeInfo(read_only=True)
    employee_profile = Profile_Serializer(read_only=True)
    class Meta:
        model = Employee
        fields = ['pk','email','surname','other_names','country','national_id','role','date_of_birth','emergency_information','payment_information','employmentinformation','employee_profile']

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

class DeleteUserSerializer(serializers.Serializer):
    """This defines the parameters to be used in assigning roles

    Args:
        serializers ([type]): [description]
    """
    user = serializers.CharField(max_length=50)

    def save(self):
        user = (self.validated_data['user'])
        try:
            user = Employee.objects.get(pk = user)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()

        except Exception as e:
            raise serializers.ValidationError(e)