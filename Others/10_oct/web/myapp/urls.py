from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('',views.index,name='main'),
    path('home',views.home,name='home'),
    path('login',views.log,name='log'),
    path('userhome',views.userhome,name='Userhome'),
    path('check',views.check,name='exam'),
    path('logout',views.logt,name='logt'),
    path('exam',views.exam,name='exam'),
    path('quiz/<id>/',views.quizz,name='quiz'),
    path('signup',views.signup,name='signup'),
    path('staff',views.sta,name='staff'),
    path('add_qt',views.addqt,name='add_qt'),
    path('del_id/<id>/',views.delte,name='delete'),
]
