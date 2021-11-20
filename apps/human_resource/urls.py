from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('api/employees/', views.EmployeeView.as_view(),name="employees"),  # list of employees
    path('api/employees/<str:employee_id>/', views.EmployeeDetail.as_view(),name="employee-detail"), # single employee
    path('api/leaves/', views.LeaveView.as_view(),name="leaves"), # list of leaves
    path('api/departments/', views.DepartmentView.as_view(),name="departments"), # list departments
    path('api/employment_types/', views.EmploymentTypeView.as_view(),name="employment_types"), # list employment types
    path('api/bank_details/', views.BankDetailsView.as_view(),name="bank_details"), # list bank details
    path('api/leaves/<str:id>/approve/', views.ApproveLeave.as_view(),name="leave-approve"), # approve leave
    path('api/jobs/', views.JobListingView.as_view(),name="jobs"), # list jobs
]