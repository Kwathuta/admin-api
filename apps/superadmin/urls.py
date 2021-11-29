from django.urls import include,path
from rest_framework.authtoken import views as token_views

from apps.superadmin import views

urlpatterns = [
   path("register_company/",views.CompanyCreation.as_view(),name="register_company"),
   path("register/",views.UserView.as_view(),name="register"),
   path('login/', views.LoginView.as_view(),name="login"),
   path('change_role/',views.ChangeRole.as_view(),name="change_role"),
   path('role/',views.RoleView.as_view(),name="roles"),
   path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
   path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
   path('delete/',views.DeleteUser.as_view(),name='delete_user'),
   path("user/<token>",views.UserDetailsView.as_view(),name="get_details"),
   path("employee/<int:id>",views.EmployeeDetailsView.as_view(),name="get_employee_details"),
   path('employee',views.AllEmployeeView.as_view(),name="employees"),
   path('role/<int:role_id>',views.RoleView.as_view(),name="role_employees"),
]
