from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('api/employees/', views.EmployeeView.as_view(),name="employees"),  # list of employees
    path('api/employees/<str:employee_id>/', views.EmployeeDetail.as_view(),name="employee-detail"), # single employee
    path('api/listing/', views.ListingView.as_view(),name="listing"), 
    path('api/leaves/', views.LeaveView.as_view(),name="leaves"),
    path('api/upload/', views.UploadFileView.as_view(), name='upload-file')
]
