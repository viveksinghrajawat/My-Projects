from django.urls import path
from . import views
urlpatterns = [
    path('',views.log,name='login'),
    path('signup',views.signup,name='signup'),
    path('reg',views.reg,name='reg'),
    path('succes',views.succ,name='succes'),
    path('quiz_start',views.qstart,name='qstart'),
    path('logt',views.logt,name='logt'),
    path('home',views.home,name='home'),
    path('quiz/<id>/',views.quizz,name='quiz'),
]