from django.urls import include,path
from rest_framework.authtoken import views as token_views

from apps.superadmin import views

urlpatterns = [
   path("register/",views.UserView.as_view(),name="register"),
   path('login/', views.LoginView.as_view(),name="login"),
   path('change_role/',views.RoleView.as_view(),name="change_role"),
]
