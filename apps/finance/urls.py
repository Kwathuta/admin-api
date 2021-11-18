from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    url(r'api/approve/(?P<pk>[0-9]+)/$', views.ApproveDetail.as_view()), # list of employee
    url(r'^api/approvew/', views.ApproveList.as_view()), # single employee
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)