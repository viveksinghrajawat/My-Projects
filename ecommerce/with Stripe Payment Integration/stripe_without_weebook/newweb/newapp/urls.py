from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('', views.home_page, name='home_Page'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_in', views.sign_in_page, name='sign_in'),
    path('sign_up', views.sign_up_page, name='sign_up'),
    path('myorder', views.my_orders, name='myorder'),
    path('mycart', views.my_cart, name='mycart'),
    path('success/<id>', views.success, name='success'),
    path('failed/<id>', views.failed, name='failed'),
    path('success_cart', views.success_cart, name='success_cart'),
    path('failed_cart', views.failed_cart, name='failed_cart'),
    path('cart_payment', views.cart_payment_page, name='cart_payment'),
    path('payment/<id>/', views.payment_page, name='payment'),
    path('add/<id>/', views.add_to_cart, name='add'),
    path('add_quantity/<id>/', views.add_quantity, name='add_quantity'),
    path('remove_quantity/<id>/', views.remove_quantity, name='remove_quantity'),
    path('add_quantity_home/<id>/', views.add_quantity_home, name='add_quantity_home'),
    path('remove_quantity_home/<id>/', views.remove_quantity_home, name='remove_quantity_home'),
    path('remove/<id>/', views.remove_from_cart, name='remove'),
    path('remove_cart/<id>/', views.cart_remove, name='remove_cart'),
    path('create-checkout-session/<pk>', views.create_checkout_session, name='create-checkout-session'),
    path('webhooks/stripe/', views.webhook,name='webhook'),
    path('create-checkout-session-cart', views.create_checkout_session_cart, name='create-checkout-session-cart'),

    # path('', include('payments.urls')),
]
