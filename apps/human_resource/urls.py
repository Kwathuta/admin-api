from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('api/employees/', views.EmployeeView.as_view(),name="employees"),  # list of employees
]
