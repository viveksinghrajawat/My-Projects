from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='home'),
    path('reg',views.regis,name="reg"),
    path('login',views.login,name="reg"),
    path('log',views.check,name="reg"),
]