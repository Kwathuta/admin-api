from django.contrib import admin
from apps.human_resource.models import EmploymentInformation

# Register your models here.
from apps.superadmin.models import *
admin.site.register(Company)
admin.site.register(Role)
admin.site.register(EmploymentInformation)
