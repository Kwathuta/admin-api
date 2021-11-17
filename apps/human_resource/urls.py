from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^api/employees/$', views.EmployeeViewSet.as_view()),  # list of employees
]
