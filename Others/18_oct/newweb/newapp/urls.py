from . import views
from django.urls import include, path

urlpatterns = [

    path('',views.home_page,name='home_Page'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('sign_in', views.sign_in_page,name='sign_in'),
    path('sign_up', views.sign_up_page,name='sign_up'),
    path('myorder', views.my_orders,name='myorder'),
    path('create-checkout-session/<pk>', views.create_checkout_session, name='create-checkout-session'),
    path('success', views.success,name='success'),
    path('cancel', views.cancel,name='cancel'),
    path('webhooks/stripe/', views.webhook,name='webhook'),
    # path('success',views.success_page,name='success_Page'),
    # path('', include('payments.urls')),
]
