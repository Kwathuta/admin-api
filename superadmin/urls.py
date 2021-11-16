from django.urls import include,path

from superadmin import views

urlpatterns = [
    path("register/",views.UserView.as_view(),name="register")
]
