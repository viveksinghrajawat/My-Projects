from datetime import  datetime, timedelta
from multiprocessing.util import is_abstract_socket_namespace
from django.shortcuts import HttpResponse
import pytz,random
from .models import *
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
def delte(request,id):
    attempt.objects.filter(id=id).delete()
    return redirect('staff')

def addqt(request):
    if request.method=='POST':
        b=quiz(question=request.POST.get('quest'),opt_1=request.POST.get('opt1'),opt_2=request.POST.get('opt2'),opt_3=request.POST.get('opt3'),opt_4=request.POST.get('opt4'))
        b.save()
        ids=quiz.objects.filter(question=request.POST.get('quest')).get()
        d=answer(quest=ids,right_ans=request.POST.get('rightans'))
        d.save()
        return redirect('/staff')

    return render(request,'myapp/quest.html')

def sta(request):
    data=attempt.objects.all().order_by('user')
    Total=quiz.objects.all().count()
    return render(request,'myapp/stafff.html',{'data':data,'total':Total})

def index(request):
    return render(request,'myapp/Home.html') 

def log(request):
    return render(request,'myapp/Login_p.html')

def userhome(request):
    try:
        data=attempt.objects.filter(user=request.user)
        Total=quiz.objects.all().count()
        return render(request,'myapp/userhome.html',{'data':data,'total':Total})
    except:
        return render(request,'myapp/userhome.html')

def check(request):
    response=redirect('/login')
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
                    if i.is_superuser:
                        return redirect('staff')
                    return redirect('/userhome')
                else:
                    messages.info(request, 'Your password is Incorrect!')  
                    return response
        if flag==0:
            messages.info(request, 'Email not registered!')
            return response
    return response

def exam(request):
    try:
        data=attempt.objects.filter(user=request.user).get()
    except:
        user_info.objects.all().delete()
        ques=quiz.objects.first()
        que=quiz.objects.filter(id__gt=ques.id).first()
        return render(request,'myapp/exam.html' ,{'ques':ques,'id':ques.id,'qn':que})
    ft=data.attempt_time+timedelta(hours=24)
    print(ft.replace(tzinfo=pytz.UTC))
    if datetime.datetime.today().replace(tzinfo=pytz.UTC)<ft:
        messages.info(request, f'You Have Already given Exam !! Try again after {ft.date()} {ft.time()}')
        return redirect('/userhome')
    else:
        user_info.objects.all().delete()
        ques=quiz.objects.first()
        que=quiz.objects.filter(id__gt=ques.id).first()
        return render(request,'myapp/exam.html' ,{'ques':ques,'id':ques.id,'qn':que})
    

def quizz(request,id):
    if request.method == "POST":   
        b=user_info(id_ques=id)
        ques=quiz.objects.filter(id=id).get()
        opt=answer.objects.get(quest=ques.id)
        if opt.right_ans==request.POST.get('answer'):
            b.answer=1
        b.save()
        try:
            b=user_info.objects.all()
            ids=[]
            for i in b:
                ids.append(i.id_ques)
            print(ids)
            items=list(quiz.objects.exclude(id__in=ids).all())
            ques=random.choice(items)
            ids.append(ques.id)
            try:
                que=quiz.objects.exclude(id__in=ids).first()
                return render(request,'myapp/exam.html' ,{'ques':ques,'id':ques.id,'qn':que})
            except:
                return render(request,'myapp/exam.html' ,{'ques':ques,'id':ques.id})
        except:
            data=user_info.objects.all()
            score=0
            for i in data:
                if i.answer==1:
                    score+=1
            b=attempt(user=request.user,attempt_time=datetime.datetime.today(),score=score)
            b.save()
            return redirect('/userhome') 
       

def logt(request):
    response=redirect('/')
    logout(request)
    return response


def home(request):
    return render(request,'myapp/Home.html')

def signup(request):
    if request.method=='POST':
        b=User(first_name=request.POST.get('fname'),last_name=request.POST.get('lname'),email=request.POST.get('email'),password=make_password(request.POST.get('password')),username=request.POST.get('username'))
        b.save()
        return redirect('login')
    return render(request,'myapp/signup.html')

