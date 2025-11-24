import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import product, user_info

def success_page(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,'newapp/success.html')


def sign_in_page(request):
    if request.method == "POST":
        input_user_name = request.POST.get("username")
        input_password = request.POST.get("password")
        import pdb;pdb.set_trace()
        user_valid = authenticate(request, username=input_user_name, password=input_password)
        if user_valid is not None:
            login(request,user=user_valid)
            return redirect('/')
        else:
            messages.info(request, 'username or password is not matched')
            return redirect('/sign_in')
    return render(request, 'newapp/sign_in_page.html')


def sign_up_page(request):
    if request.method == 'POST':
        try:
            User.objects.create_user(first_name = request.POST.get('fname'), last_name = request.POST.get('lname'), email = request.POST.get('email'), password = request.POST.get('password'), username = request.POST.get('username'))
            # user.save() not needed
            return redirect('/sign_in')
        except:
            messages.info(request,'error occured try again')
            return redirect('/sign_up')
    return render(request, 'newapp/sign_up_page.html')

@login_required(login_url='/sign_in')
def sign_out(request):
    # import pdb;pdb.set_trace()
    logout(request) 
    return redirect('/')

@login_required(login_url='/sign_in')
def user_home_page(request,id):
    if id:
        product_info=product.objects.get(pk=id)
        import pdb;pdb.set_trace()
        if  product_info:
            data=User.objects.filter(username=request.user)
            user_info.objects.create(user=request.user,product_name=product_info,buy_time=datetime.datetime.now(),payment_satuts='success')
            status='Succesfull'
            return render(request,'newapp/success.html',{'product_info':product_info,'userdata':data,'status':status})

@login_required(login_url='/sign_in')
def my_orders(request):
    order_data=user_info.objects.filter(user=request.user)
    return render(request, 'newapp/my_order.html', context={'orderdata':order_data })

@login_required(login_url='/sign_in')
def fail_page(request, id):
    if id:
        product_info = product.objects.filter(id=id).get()
        data = User.objects.filter(username=request.user)
        user_info.objects.create(user=request.user,product_name=product_info,buy_time=datetime.datetime.now(),payment_satuts='Failed')
        status = 'Failed'
        return render(request, 'newapp/failed.html',{'product_info':product_info,'userdata':data,'status':status})

def home_page(request):
    # request.session.flush()
    product_data=product.objects.all()
    return render(request, 'newapp/home_page.html', context={'product_data':product_data })