from django.urls import include,path
from rest_framework.authtoken import views as token_views

from superadmin import views

urlpatterns = [
    path("register/",views.UserView.as_view(),name="register"),
    path('login/', token_views.obtain_auth_token)
]
