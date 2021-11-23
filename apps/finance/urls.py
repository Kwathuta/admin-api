from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    url(r'api/approve/(?P<pk>[0-9]+)/$', views.ApproveDetail.as_view()), # single employee
    url(r'^api/approvew/', views.ApproveList.as_view()), # list of employee
    url(r'^api/message/',views.MessageList.as_view()),
    url(r'api/staff/(?P<pk>[0-9]+)/$', views.StaffDetail.as_view()), # single of staff
    url(r'^api/staffw/', views.StaffList.as_view()), # list of staff
    url(r'api/pay/(?P<pk>[0-9]+)/$', views.PayDetail.as_view()), # single payroll
    url(r'^api/payw/', views.PayList.as_view()), # list payroll
    #url(r'^api/expensesw/', views.ExpensesList.as_view()), # list of expense
    #url(r'api/expenses/(?P<pk>[0-9]+)/$', views.ExpenseDetail.as_view()), # single expense
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)