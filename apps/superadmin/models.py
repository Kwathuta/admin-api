from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db.models.deletion import CASCADE, PROTECT
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group

# Create your models here.
class CompanyTypes(models.Model):
    """This defines the possible options for the company types

    Args:
        models ([type]): [description]

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    """This defines the fields within the company

    Args:
        models ([type]): [description]

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    name = models.CharField(max_length=100)
    number_of_staff = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    headquarters = models.CharField(max_length=50,null=True)
    contact_email = models.EmailField(null=True)
    branches = models.IntegerField(null=True)
    type = models.ForeignKey(CompanyTypes,on_delete=models.PROTECT,null=True)
    company_logo = models.ImageField(null=True,upload_to="company_logo/")

class Role(models.Model):
    """This defines the new roles a user can have

    Args:
        models ([type]): [description]

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    name = models.CharField(max_length=30,verbose_name="The role of a user in the organisation")

    def __str__(self):
        return self.name


# class MyAccountManager(BaseUserManager):
#     """defines the methods to manage the custom user to be created

#     Args:
#         BaseUserManager ([type]): [description]

#     Returns:
#         [type]: [description]
#     """

#     def create_user(self, email, username, password=None,role=None):
#         if not email:
#             raise ValueError("Users must have and email address")

#         if not username:
#             raise ValueError("You must have a username")


#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             password=password
#         )
#         user.role = Role.objects.get(name="subordinate_staff")
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password
#         )
#         user.is_admin = True
#         user.is_superuser = True
#         user.is_staff = True
#         user.role = Role.objects.get(name="super_admin")

#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     """This will define the custom user model to be used

#     Args:
#         AbstractBaseUser ([type]): [description]
#     """

#     email = models.EmailField(verbose_name="email",
#                               max_length=100, unique=True)

#     username = models.CharField(max_length=30)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     nationality = models.CharField(max_length=30)
#     national_id = models.IntegerField(
#         verbose_name="National Id or passport", null=True)
#     date_joined = models.DateTimeField(
#         verbose_name="date joined", auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     role = models.ForeignKey(Role,on_delete=models.PROTECT)
#     objects = MyAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True

#     def delete_user(self):
#         self.delete()

#     def change_group(self,role):
#         """This will change a user's group

#         Returns:
#             [type]: [description]
#         """
#         self.role = role
#         self.save()

class MyAccountManager(BaseUserManager):
    """defines the methods to manage the custom user to be created

    Args:
        BaseUserManager ([type]): [description]

    Returns:
        [type]: [description]
    """

    def create_user(self, email, password=None,role=None,surname=None):
        if not email:
            raise ValueError("Users must have and email address")

        user = self.model(
            email=self.normalize_email(email),
            surname = surname,
            password=password
        )
        user.role = Role.objects.get(name="subordinate_staff")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password,surname=None):
        user = self.create_user(
            email=self.normalize_email(email),
            surname = surname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.get(name="super_admin")

        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser):
    """This is the user instance

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    employee_id = models.CharField(primary_key=True,unique=True,null=False,max_length=50)
    surname = models.CharField(max_length=30)
    other_names = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='work email',unique=True)
    national_id = models.CharField(max_length=8)
    role = models.ForeignKey(Role,on_delete=models.PROTECT)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=100)
    # phone_number = models.CharField(max_length=100,null=True)

    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['surname']

    def __str__(self):
        return self.username

    @classmethod
    def get_employee_by_id(cls, employee_id):
        employee = cls.objects.get(employee_id=employee_id)
        return employee
    
    # get all employees where status is active
    @classmethod
    def get_all_active_employees(cls):
        employees = cls.objects.filter(status='active')
        return employees

    def __str__(self):
        return self.surname

MARRIED = "married"
SINGLE = "single"
DIVORCED = "divorced"
WIDOW = "widow"
marital_choices = (
    (MARRIED,'married'),
    (SINGLE,'single'),
    (DIVORCED,'divorced'),
    (WIDOW,'widow')
)


class EmployeeProfile(models.Model):
    """This is the employees personal and changeable information

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    employee = models.OneToOneField(Employee,on_delete=CASCADE,related_name="employee_profile")
    personal_email = models.EmailField(verbose_name="personal email",null=True)
    profile_pic = models.ImageField(upload_to="profile/",null=True)
    marital_status = models.CharField(choices=marital_choices,null=True,max_length=50)
    insurance_number = models.CharField(max_length=20,null=True)
    phone_number = PhoneNumberField(region="KE")

    def __str__(self):
        return self.employee.surname + "'s profile"

class PaymentInformation(models.Model):
    """This contains the payment information for a user

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    employee = models.OneToOneField(Employee,on_delete=CASCADE,related_name="payment_information")
    bank_name = models.CharField(max_length=30,null=True)
    branch = models.CharField(max_length=30,null=True)
    account_number = models.CharField(max_length=20,null=True)
    gross_pay = models.DecimalField(decimal_places=2,max_digits=10,null=True)

    def __str__(self):
        return self.employee.surname + "'s payment details"

class EmergencyRelationships(models.Model):
    """A list of relationships that can be used to define a user's relationship with the emeregency contact
    """
    name = models.CharField(
        max_length=20, verbose_name="Name of relationship", null=False)

    class Meta:
        verbose_name = "Emergency relationship"
        verbose_name_plural = "Emergency relationships"

    def __str__(self):
        return self.name


class EmergencyInformation(models.Model):
    """These entail a user's go to information in case of an emergency
    """
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name="emergency_information")
    name = models.CharField(
        max_length=20, verbose_name="Emergency contact's name", null=True)
    phone_number = PhoneNumberField(
        null=True,region="KE", verbose_name="Emergency contact's phone number")
    relationship = models.ForeignKey(
        EmergencyRelationships, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.surname + "'s emergency information"

    class Meta:
        verbose_name = "Emergency information"
        verbose_name_plural = "Emergency informations"

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
