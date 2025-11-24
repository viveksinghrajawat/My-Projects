from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('',views.home_page,name='home_Page'),
    path('user_home/<id>/', views.user_home_page, name='userhome'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('success', views.success_page, name='success_page'),
    path('sign_in', views.sign_in_page,name='sign_in'),
    path('sign_up', views.sign_up_page,name='sign_up'),
    path('myorder', views.my_orders,name='myorder'),
    path('failed/<id>/', views.fail_page,name='failed'),
    # path('success',views.success_page,name='success_Page'),
    # path('', include('payments.urls')),
]
