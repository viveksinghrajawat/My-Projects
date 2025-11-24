from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('',views.home_page,name='home_Page'),
    path('success', views.success_page, name='success_page'),
    # path('success',views.success_page,name='success_Page'),
    # path('', include('payments.urls')),
]
