from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class MyAccountManager(BaseUserManager):
    """defines the methods to manage the custom user to be created

    Args:
        BaseUserManager ([type]): [description]

    Returns:
        [type]: [description]
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have and email address")

        if not username:
            raise ValueError("You must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """This will define the custom user model to be used

    Args:
        AbstractBaseUser ([type]): [description]
    """

    email = models.EmailField(verbose_name="email",
                              max_length=100, unique=True)

    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    national_id = models.IntegerField(
        verbose_name="National Id or passport", null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def delete_user(self):
        self.delete()


MALE = 'male'
FEMALE = 'female'
RATHER_NOT_SAY = 'rather_not_say'
gender_choices = (
    (MALE, 'male'),
    (FEMALE, 'female'),
    (RATHER_NOT_SAY, 'rather_not_say')
)


class Profile(models.Model):
    """This entails a user's common details
    """
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    work_email = models.EmailField(
        verbose_name="work email", unique=True, null=True)
    personal_email = models.EmailField(
        verbose_name="personal email", null=True, unique=True)
    mobile_number = PhoneNumberField(region="KE", null=True)
    profile_pic = models.ImageField(upload_to="profile/", null=True)
    insurance_number = models.CharField(max_length=20, null=True)
    marital_status = models.BooleanField(null=True)
    gender = models.CharField(max_length=20, choices=gender_choices, null=True)

    def __str__(self):
        return self.employee.username + "'s " + "profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class EmploymentInformation(models.Model):
    """This entails the users connection with the company
    """
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    employment_date = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=20, null=True)
    employment_type = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=True)
    country = models.CharField(max_length=20, null=True)
    company_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.employee.username + "'s employee info"

    class Meta:
        verbose_name = "Employment Information"
        verbose_name_plural = "Employment Information"


class PaymentInformation(models.Model):
    """This entails a user's payment information
    """
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    bank = models.CharField(max_length=20, null=True)
    branch = models.CharField(max_length=20, null=True)
    account_number = models.CharField(max_length=20, null=True)
    gross_pay = models.DecimalField(null=True, decimal_places=2, max_digits=9)
    net_pay = models.DecimalField(null=True, decimal_places=2, max_digits=9)

    def __str__(self):
        return self.employee.username + "'s payment_info"

    class Meta:
        verbose_name = "Payments Information"
        verbose_name_plural = "Payment Information"


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
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=20, verbose_name="Emergency contact's name", null=True)
    phone = PhoneNumberField(
        null=True, verbose_name="Emergency contact's phone number")
    relationship = models.ForeignKey(
        EmergencyRelationships, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.username + "'s emergency information"

    class Meta:
        verbose_name = "Emergency information"
        verbose_name_plural = "Emergency informations"
