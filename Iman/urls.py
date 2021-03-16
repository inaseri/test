from django.urls import path
from . import views
import absenteeism
from absenteeism.views import index,adminT
from django.conf.urls import url,include
from Iman.resource import CompaniesResource, TransactionsResource, BankResource
from tastypie.api import Api


v1_api = Api(api_name='v1')
v1_api.register(CompaniesResource())
v1_api.register(TransactionsResource())
v1_api.register(BankResource())


urlpatterns = [
    path('', absenteeism.views.index, name='index'),
    path(r'adminOfTimeSite/',absenteeism.views.adminT, name='admint'),
    path(r'accounts/login/', views.clogin, name="login"),
    path(r'accounts/logout/',views.clogout,name="logout"),
    path(r'addtransaction/', views.caddtransaction, name='add_transaction'),
    path(r'addcompany/',views.caddcompany, name="addcompany"),
    path(r'transactions/',views.index, name="transactions"),
    url(r'^export/csv/$', absenteeism.views.index, name='export_users_csv'),
    path(r'getVacation/', absenteeism.views.vecation, name='getVacation'),
    url(r'^api/', include(v1_api.urls)),
]


