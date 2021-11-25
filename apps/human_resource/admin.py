from django.contrib import admin

from .models import Employee, EmploymentType, Department, BankDetails, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter,EmploymentInformation,PaymentInformation



admin.site.register(Employee)
admin.site.register(EmploymentType)
admin.site.register(Department)
admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(BankDetails)
admin.site.register(EmploymentInformation)
admin.site.register(PaymentInformation)