from django.urls import include,path
from rest_framework.authtoken import views as token_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import url

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from apps.superadmin import views

urlpatterns = [
    path("register/",views.UserView.as_view(),name="register"),
    path('login/', token_views.obtain_auth_token),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
