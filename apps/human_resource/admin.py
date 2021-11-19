from django.contrib import admin
from .models import Employee,BulkEmployee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter



admin.site.register(Employee)
admin.site.register(EmploymentType)
admin.site.register(Department)
admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(BankDetails)
admin.site.register(BulkEmployee)