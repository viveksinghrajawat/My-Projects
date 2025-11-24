from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('',views.home_page,name='home_Page'),
    path('sign_in',views.sign_in_page,name='sign_in'),
    path('sign_up',views.sign_up_page,name='sign_up'),
    path('user_home',views.user_home_page,name='user_home'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('start_quiz',views.start_quiz,name='start_quiz'),
    path('quiz/<id>/',views.quiz,name='quiz'),  
    path('staff_user',views.staff_user_page,name='staff_user'),
    path('delete_user/<id>/',views.delete_user_details,name='delete_user'),
    path('add_question',views.add_more_questions,name='add_question')
]
