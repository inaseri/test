from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name='index'),
    path(r'admint/', views.adminT, name='admint'),
    url(r'^export/xls/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.export_users_xls, name='export_users_xls'),
    path(r'change/<int:id>', views.changeTime, name='changeTime'),
]


