from datetime import  datetime, timedelta
import pytz,random
from .models import *
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def home_page(request):
    return render(request,'myapp/home_page.html') 

def sign_in_page(request):
    if request.method == "POST":
        input_user_name = request.POST.get("username")
        input_password = request.POST.get("password")
        # import pdb;pdb.set_trace()
        user_valid = authenticate(request, username = input_user_name, password = input_password)
        if user_valid is not None:
            if user_valid.is_superuser:
                login(request,user = user_valid)
                return redirect('/staff_user')
            login(request,user=user_valid)
            return redirect('/user_home')
        else:
            messages.info(request, 'username or password is not matched')
            return redirect('/sign_in')
    return render(request, 'myapp/sign_in_page.html')

def sign_up_page(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), email = request.POST.get('email'), password = request.POST.get('password'), username = request.POST.get('username'))
            user.save()
            return redirect('/sign_in')
        except:
            messages.info(request,'error occured try again')
            return redirect('/sign_up')
    return render(request, 'myapp/sign_up_page.html')

@login_required(login_url='/sign_in')
def sign_out(request):
    logout(request) 
    return redirect('/')

#Staff  user views
@login_required(login_url='/sign_in')
def staff_user_page(request):
    all_user_data = User_Information.objects.all()
    user_data = User.objects.filter(is_staff=False).all()
    Total_marks = Quiz_model.objects.all().count()
    return render(request, 'myapp/staff_user_home_page.html', {'data':all_user_data, 'userdata':user_data, 'total':Total_marks})

@login_required(login_url='/sign_in')
def delete_user_details(request,id):
    User_Information.objects.filter(id = id).delete()
    return redirect('/staff_user')

@login_required(login_url='/sign_in')
def add_more_questions(request):
    if request.method == 'POST':
        question_obj = Quiz_model.objects.create(question=request.POST.get('quest'), option_1=request.POST.get('opt1'), option_2=request.POST.get('opt2'), option_3=request.POST.get('opt3'), option_4=request.POST.get('opt4'))
        question_obj.save()
        question_obj_id = Quiz_model.objects.filter(question=request.POST.get('quest')).get()
        question_obj_answer = Answer_Model.objects.create(question=question_obj_id, right_ans=request.POST.get('rightans'))
        question_obj_answer.save()
        return redirect('/staff_user_home')

    return render(request, 'myapp/add_question.html')

#user views
@login_required(login_url='/sign_in')
def user_home_page(request):
    try:
        user_data = User_Information.objects.filter(user=request.user)
        Total_Marks = Quiz_model.objects.all().count()
        return render(request,'myapp/user_home_page.html', {'data':user_data, 'total':Total_Marks})
    except:
        return render(request,'myapp/user_home_page.html')
    
@login_required(login_url='/sign_in')
def start_quiz(request):
    try:
        user_previous_exam_data = User_Information.objects.filter(user=request.user).get()
    except:
        Score_Calculator.objects.all().delete()
        question = Quiz_model.objects.first()
        next_question = Quiz_model.objects.filter(id__gt = question.id).first() #checking if next question exist
        return render(request, 'myapp/quiz_page.html', {'question':question, 'id':question.id, 'next_question':next_question})
    next_exam_date = user_previous_exam_data.attempt_time + timedelta(hours = 24)
    if datetime.today().replace(tzinfo=pytz.UTC) < next_exam_date:
        messages.info(request, f'You Have Already given Exam !! Try again after {next_exam_date.date()} {next_exam_date.time()}')
        return redirect('/user_home')
    else:
        Score_Calculator.objects.all().delete()
        question = Quiz_model.objects.first()
        next_question = Quiz_model.objects.filter(id__gt=question.id).first() #checking if next question exist
        return render(request,'myapp/quiz_page.html', {'question':question, 'id':question.id, 'next_question':next_question})
    
@login_required(login_url='/sign_in')
def quiz(request,id):
    if request.method == "POST":   
        score_obj = Score_Calculator(question_id=id)
        question = Quiz_model.objects.filter(id=id).get()
        question_right_answer = Answer_Model.objects.get(question=question.id)
        user_answer = request.POST.get('answer')
        if question_right_answer.right_answer == user_answer:
            score_obj.marks_user = 1
            score_obj.save()
        else:
            score_obj.save()    
        
        try:
            score_data=Score_Calculator.objects.all()
            question_ids = []
            for data in score_data:
                question_ids.append(data.question_id)
            question_list = list(Quiz_model.objects.exclude(id__in = question_ids).all())
            random_question = random.choice(question_list)
            question_ids.append(random_question.id)
            try:
                next_question = Quiz_model.objects.exclude(id__in = question_ids).first()
                return render(request, 'myapp/quiz_page.html', {'question':random_question, 'id':random_question.id, 'next_question':next_question})
            except:
                return render(request, 'myapp/quiz_page.html', {'question':random_question, 'id':random_question.id})
        except:
            score = Score_Calculator.objects.all()
            marks = 0
            for data in score:
                if data.marks_user == 1:
                    marks += 1
            user_data = User_Information.objects.create(user = request.user, attempt_time = datetime.today(), score = marks)
            user_data.save()
            return redirect('/user_home') 