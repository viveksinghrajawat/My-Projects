from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('', views.home_page, name='home_Page'),
    path('user_home/<id>/', views.user_home_page, name='userhome'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_in', views.sign_in_page, name='sign_in'),
    path('sign_up', views.sign_up_page, name='sign_up'),
    path('paymenthandler/<id>', views.paymenthandler, name='paymenthandler'),
    path('myorder', views.my_orders, name='myorder'),
    path('mycart', views.my_cart, name='mycart'),
    path('cart_payment_success', views.cart_success, name='cart_success'),
    path('cart_payment_failed', views.cart_failed, name='cart_failed'),
    path('cart_payment', views.cart_payment_page, name='cart_payment'),
    path('failed/<id>/', views.fail_page, name='failed'),
    path('payment/<id>/', views.payment_page, name='payment'),
    path('add/<id>/', views.add_to_cart, name='add'),
    path('add_quantity/<id>/', views.add_quantity, name='add_quantity'),
    path('remove_quantity/<id>/', views.remove_quantity, name='remove_quantity'),
    path('add_quantity_home/<id>/', views.add_quantity_home, name='add_quantity_home'),
    path('remove_quantity_home/<id>/', views.remove_quantity_home, name='remove_quantity_home'),
    path('remove/<id>/', views.remove_from_cart, name='remove'),
    path('remove_cart/<id>/', views.cart_remove, name='remove_cart'),
    
    # path('success',views.success_page,name='success_Page'),
    # path('', include('payments.urls')),
]
