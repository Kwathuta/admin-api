from django.contrib import admin

from .models import Employee, EmploymentType, Department, LeaveType, Leave, JobListing, Application, ScheduledInterview, OfferLetter, EmploymentInformation, PaymentInformation, EmployeeProfile


admin.site.register(Employee)
admin.site.register(EmploymentType)
admin.site.register(Department)
admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(EmploymentInformation)
admin.site.register(PaymentInformation)
admin.site.register(EmployeeProfile)
