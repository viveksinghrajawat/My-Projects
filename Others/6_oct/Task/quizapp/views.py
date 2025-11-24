from datetime import  datetime, timedelta
from django.shortcuts import HttpResponse, redirect
from .models import *
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
# Create your views here.
import pytz

utc=pytz.UTC

def log(request):
    return render(request,'quizapp/login.html')


def logt(request):
    response=redirect('/')
    logout(request)
    return response


def succ(request):
    data=user_info.objects.all()
    marks=0
    for i in data:
        if i.answer==1:
            marks+=1
    b=attempt(user=request.user,test_name='python',attempt_time=datetime.datetime.today(),score=marks)
    b.save()
    total=quiz.objects.all().count()
    return render(request,'quizapp/succ.html',{'marks':marks,'total':total})

def signup(request):
    return render(request,'quizapp/signup.html')


def qstart(request):
    # b=attempt(user=request.user,test_name='python',attempt_time=datetime.today().date(),score='0')        
    # b.save()
    try:
        data=attempt.objects.filter(user=request.user).get()
    except:
        user_info.objects.all().delete()
        ques=quiz.objects.first()
        que=quiz.objects.filter(id__gt=ques.id).first()
        return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id,'qn':que})
    ft=data.attempt_time+timedelta(hours=24)
    print(ft.replace(tzinfo=pytz.UTC))
    if datetime.datetime.today().replace(tzinfo=pytz.UTC)<ft:
        messages.info(request, f'You Have Already given Exam !! Try again after {ft.date()} {ft.time()}')
        return redirect('home')
    else:
        user_info.objects.all().delete()
        ques=quiz.objects.first()
        que=quiz.objects.filter(id__gt=ques.id).first()
        return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id,'qn':que})

def reg(request):
    response=redirect('/')
    # import pdb;pdb.set_trace()
    if request.method=='POST':
        b=User(first_name=request.POST.get('fname'),last_name=request.POST.get('lname'),email=request.POST.get('email'),password=make_password(request.POST.get('password')),username=request.POST.get('username'))
        b.save()
    # return render(request,'quizapp/home.html')
    return response

def quizz(request,id):
    response=redirect('/')
    if request.method == "POST":   
        b=user_info(id_ques=id)
        ques=quiz.objects.filter(id=id).get()
        if ques.right_ans==request.POST.get('answer'):
            b.answer=1
        b.save()
        try:
            ques=quiz.objects.filter(id__gt=id).first()
            try:
                que=quiz.objects.filter(id__gt=ques.id).first()
                return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id,'qn':que})
            except:
                return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id})
            
            
        except:
            data=user_info.objects.all()
            score=0
            for i in data:
                if i.answer==1:
                    score+=1
            return redirect('succes') 
    return response        
        
        # else:
        #     b=attempt(user=request.user,test_name='python',attempt_time=datetime.today().date())
        #     
        #     b.save()
        #     return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id})   
            # return render(request,'quizapp/quiz.html' ,{'ques':ques,'id':ques.id})
            # return render(request,'quizapp/quiz.html')

def home(request):
    response=redirect('/')
    if request.method == "POST":
        data=User.objects.all()
        em=request.POST.get("email")
        flag=0
        for i in data:
            if i.email==em:
                flag=1
                pss=request.POST.get("password")
                if check_password(pss,i.password):
                    data=attempt.objects.filter(user=i.id)
                    login(request,user=i)
                    return render(request,'quizapp/home.html',{'data':data})
                else:
                    messages.info(request, 'Your password is Incorrect!')  
                    return response
        if flag==0:
            messages.info(request, 'Email not registered!')
            return response
    try:
        data=attempt.objects.filter(user=request.user)
        return render(request,'quizapp/home.html',{'data':data})
    except:
        return response
    