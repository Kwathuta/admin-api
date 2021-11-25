from django.db import models
import datetime as dt

# cloudinary
from cloudinary.models import CloudinaryField
from apps.superadmin.models import *



# =================== Employee Management start tables ===================

# employment Type
class EmploymentType(models.Model):
    """
        Employment Type
    """
    name = models.CharField(max_length=100)
    
    def  __str__(self):
        return self.name

# departments model 
class Department(models.Model):
    """
        Department Model
    """
    
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# payment details model
class BankDetails(models.Model):
    """
        Payment details model
    """
    
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    
    def __str__(self):
        return self.bank_name


class EmploymentInformation(models.Model):
    """The employee relation with the company
    Args:
        models ([type]): [description]
    """
    employee = models.OneToOneField(Employee,on_delete=CASCADE,related_name="employment_information")
    company = models.ForeignKey(Company,on_delete=models.PROTECT,null=True,related_name="employees")
    employment_date = models.DateField(auto_now_add=True,editable=True)
    position = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    department = models.ForeignKey(Department,on_delete=models.PROTECT,null=True)
    employment_type = models.ForeignKey(EmploymentType,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.employee.surname + "'s employment info"

# leave Category model
class LeaveType(models.Model):
    """
        Type of leave
    """
    
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# leave model
class Leave(models.Model):
    """
        Leave model
    """
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="employee_leave")
    positon = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE,null=True)
    leave_date_from = models.DateField(null=True, blank=True)
    leave_date_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # soft_delete = models.BooleanField(default=False)
    
    # get all employees where status is approve and date to is greater than today
    @classmethod
    def get_all_approved_leaves_and_active(cls):
        leaves = cls.objects.filter(status='approved', leave_date_to__gte=dt.date.today())
        return leaves
    # get all employees where status is approve and date to is not greater than today
    # def get_all_approved_leaves_and_inactive(self):
    #     return self.objects.filter(status='approved', leave_date_to__lt=dt.date.today())
    
    # get all leaves where status is pending and not other status
    @classmethod
    def get_all_pending_leaves(cls):
        leaves = cls.objects.filter(status='pending')
        return leaves
   
    
    def __str__(self):
        return self.employee.surname + ' - ' + self.leave_type.name + ' - ' + self.leave_date_from.strftime('%d-%m-%Y') + ' - ' + self.leave_date_to.strftime('%d-%m-%Y')
    
    
# =================== Leave Manager end ===============================


    
# =================== Hiring start ====================================


# job listing model
class JobListing(models.Model):
    """
        Job listing model
    """
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # soft_delete = models.BooleanField(default=False)
    
    # get job listing details by id
    @classmethod
    def get_job_listing_by_id(cls, job_id):
        job_listing = cls.objects.get(id=job_id)
        return job_listing
    
    # get active job listing where deadline is greater than current date
    @classmethod
    def get_active_job_listing(cls):
        active_job_listing = cls.objects.filter(deadline__gte=dt.date.today())
        return active_job_listing

    # get past job listing where deadline is less than current date
    @classmethod
    def get_past_job_listing(cls):
        past_job_listing = cls.objects.filter(deadline__lt=dt.date.today())
        return past_job_listing
    
    def __str__(self):
        return self.job_title

# application model
class Application(models.Model):
    """
        Application model
    """
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    linkedin_url = models.URLField(max_length=200)
    phone_number = models.CharField(max_length=120)
    position = models.CharField(max_length=100, null=True, blank=True)
    education_obtained = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.CharField(max_length=100, null=True, blank=True)
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    experience = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100)
    date_available = models.DateField(auto_now=True)
    # resume = CloudinaryField('resume', null=True, blank=True)
    cover_letter = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)

    # get application details by id
    @classmethod
    def get_application_by_id(cls, application_id):
        application = cls.objects.get(id=application_id)
        return application

    # get application details by job listing id
    @classmethod
    def get_application_by_job_listing_id(cls, job_listing_id):
        application = cls.objects.filter(job_listing_id=job_listing_id)
        return application

    # get application details by applicant name
    @classmethod
    def get_application_by_applicant_name(cls, applicant_name):
        application = cls.objects.filter(applicant_name=applicant_name)
        return application

    # get application details by status
    @classmethod
    def get_application_by_status(cls, status):
        application = cls.objects.filter(status=status)
        return application

    # get past applications where created_at is more than one week ago 
    @classmethod
    def get_past_applications(cls):
        past_application = cls.objects.filter(created_at__lt=dt.date.today()-dt.timedelta(days=7))
        return past_application
    
    # get new applications where created_at is not less than one week ago
    @classmethod
    def get_new_application(cls):
        new_application = cls.objects.filter(created_at__gte=dt.date.today() - dt.timedelta(days=7))
        return new_application

    def __str__(self):
        return self.job_listing.job_title
    

# scheduled interview model
class ScheduledInterview(models.Model):
    """
        Scheduled interview model
    """
    applicant = models.ForeignKey(Application, on_delete=models.CASCADE)
    interview_date = models.DateField(auto_now=True)
    interview_time_from = models.TimeField(auto_now=True)
    interview_time_to = models.TimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)
    
    # get scheduled interview details by id
    @classmethod
    def get_scheduled_interview_by_id(cls, scheduled_interview_id):
        scheduled_interview = cls.objects.get(id=scheduled_interview_id)
        return scheduled_interview

    # get scheduled interview details by application id
    @classmethod
    def get_scheduled_interview_by_application_id(cls, application_id):
        scheduled_interview = cls.objects.filter(application_id=application_id)
        return scheduled_interview

    # get scheduled interview details by interview date
    @classmethod
    def get_scheduled_interview_by_interview_date(cls, interview_date):
        scheduled_interview = cls.objects.filter(interview_date=interview_date)
        return scheduled_interview

    # get scheduled interview details by interview time
    @classmethod
    def get_scheduled_interview_by_interview_time(cls, interview_time):
        scheduled_interview = cls.objects.filter(interview_time=interview_time)
        return scheduled_interview
    
    def __str__(self):
        return self.applicant.applicant_name
    
    

# offer letter model
class OfferLetter(models.Model):
    """
        Offer letter model
    """
    job_title = models.CharField(max_length=200)
    applicant = models.ForeignKey(Application, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    supervisor = models.CharField(max_length=200)
    offer_start_date = models.DateField(auto_now=True)
    offer_letter_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)
    
    # get offer letter details by id
    @classmethod
    def get_offer_letter_by_id(cls, offer_letter_id):
        offer_letter = cls.objects.get(id=offer_letter_id)
        return offer_letter

    # get offer letter details by application id
    @classmethod
    def get_offer_letter_by_application_id(cls, application_id):
        offer_letter = cls.objects.filter(application_id=application_id)
        return offer_letter

    # get offer letter details by offer letter date
    @classmethod
    def get_offer_letter_by_offer_letter_date(cls, offer_letter_date):
        offer_letter = cls.objects.filter(offer_letter_date=offer_letter_date)
        return offer_letter

    # get offer letter details by offer letter content
    @classmethod
    def get_offer_letter_by_offer_letter_content(cls, offer_letter_content):
        offer_letter = cls.objects.filter(offer_letter_content=offer_letter_content)
        return offer_letter
    
    # get offer letter details by applicant name
    @classmethod
    def get_offer_letter_by_applicant_name(cls, applicant_name):
        applicant_name = cls.objects.filter(applicant_name=applicant_name)
        return applicant_name
    
    def __str__(self):
        return self.applicant.applicant_name