import datetime,re
import random
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from newweb import settings
from .models import Otp, Product,User_Info,Cart
from django.core import exceptions as error
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail


def sign_in_page(request):
    if request.method == "POST":
        # import pdb;pdb.set_trace()
        input_user_name = request.POST.get("username")
        input_password = request.POST.get("password")
        # import pdb;pdb.set_trace()
        user_valid = authenticate(request, username=input_user_name, password=input_password)
        if user_valid is not None:
            login(request, user=user_valid)
            return redirect('/')
        else:
            messages.info(request, 'username or password is not matched')
            return redirect('/sign_in')
    return render(request, 'newapp/sign_in_page.html')


def sign_up_page(request):
    if request.method == 'POST':
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        input_email = request.POST.get('email')
        input_username = request.POST.get('username')
        input_first_name = request.POST.get('fname')
        input_last_name = request.POST.get('lname')
        input_password =  request.POST.get('password')
        if re.fullmatch(regex, input_email) and str(input_first_name).isalpha() and str(input_last_name).isalpha():
            try:
                User.objects.create_user(first_name=input_first_name, last_name=input_last_name, email=input_email, password=input_password, username=input_username)
                # user.save() not needed
                return redirect('/sign_in')
            except :
                messages.info(request, 'error occured try again')
                return redirect('/sign_up')
        else:
            messages.info(request, 'error occured try again')
            return redirect('/sign_up')
    return render(request, 'newapp/sign_up_page.html')


@login_required
def sign_out(request):
    # import pdb;pdb.set_trace()
    logout(request) 
    return redirect('/')


@login_required
def user_home_page(request, id):
    if id:
        try:
            product_info = Product.objects.get(pk=id)
            # import pdb;pdb.set_trace()
            data = User.objects.filter(username=request.user)
            User_Info.objects.create(user=request.user, product_name=product_info, buy_time=datetime.datetime.now(), payment_satuts='success')
            status = 'Succesfull'
            return render(request, 'newapp/success.html', {'product_info': product_info,'userdata':data,'status':status})
        except error.ObjectDoesNotExist: #to handle DoNotExist error
            return redirect('/')


@login_required
def my_orders(request):
    order_data = User_Info.objects.filter(user=request.user)
    return render(request, 'newapp/my_order.html', context={'orderdata':order_data })


@login_required
def fail_page(request, id):
    if id:
        try:
            product_info=Product.objects.get(pk=id)
            if  product_info:
                data = User.objects.filter(username=request.user)
                User_Info.objects.create(user=request.user,product_name=product_info,buy_time=datetime.datetime.now(),payment_satuts='Failed')
                status = 'Failed'
                return render(request, 'newapp/failed.html',{'product_info':product_info, 'userdata':data,'status':status})
        except error.ObjectDoesNotExist: #to handle DoNotExist error
            return redirect('/')


def home_page(request):
    # request.session.flush()
    product_data = Product.objects.all()
    if request.user.is_authenticated:
        cart_data=Cart.objects.filter(user=request.user)
        product_ids=[]
        for items in cart_data:
            product_ids.append(items.product.id)
        return render(request, 'newapp/home_page.html', context={'product_data':product_data , 'cart_data':cart_data, 'ids':product_ids })
    return render(request, 'newapp/home_page.html', context={'product_data':product_data})


@login_required
def payment_page(request,id):
    try:
        product_info = Product.objects.get(pk=id)
    except: #to handle DoNotExist error
        return redirect('/')
    return render(request, 'newapp/payment.html', context={'product_info':product_info })


@login_required
def cart_payment_page(request):
    try:
        cart_info = Cart.objects.filter(user=request.user)
        total_amount = 0
        for items in cart_info:
            total_amount += (int(float(items.product.product_price)) * items.quantity)
    except error.ObjectDoesNotExist: #to handle DoNotExist error
        return redirect('/')
    return render(request, 'newapp/cart_payment.html', context={'amount': total_amount })


@login_required
def add_to_cart(request,id):
    try:
        product_info = Product.objects.get(id=id)
        try:
            cart_data = Cart.objects.get(user=request.user, product=product_info)
            cart_data.quantity = cart_data.quantity+1
            cart_data.save()
        except error.ObjectDoesNotExist:
            Cart.objects.create(user=request.user, product=product_info, quantity = 1)
        return redirect('/')
    except error.ObjectDoesNotExist:
        return redirect('/')


@login_required
def remove_from_cart(request,id):
    try:
        product_instace_cart = Cart.objects.get(id=id)
        product_instace_cart.delete()
        return redirect('mycart')
    except error.ObjectDoesNotExist:
        return redirect('/')


@login_required
def my_cart(request):
    cart_info = Cart.objects.filter(user=request.user)
    total_amont = 0
    for items in cart_info:
        total_amont += (int(float(items.product.product_price)) * items.quantity)
    # messages.success(request, "Cart updated!!")
    return render(request, 'newapp/mycart.html', context={'cart_info':cart_info ,'total': total_amont })


@login_required
def add_quantity(request,id):
    try:
        cart_item_info = Cart.objects.get(id=id)
    except error.ObjectDoesNotExist: #to handle DoNotExist Error
        return redirect('/')
    cart_item_info.quantity += 1
    cart_item_info.save()
    return redirect('mycart')


@login_required
def remove_quantity(request,id):
    try:
        cart_item_info = Cart.objects.get(id=id)
    except error.ObjectDoesNotExist: #to handle DoNotExist Error
        return redirect('/')
    if cart_item_info.quantity >1:
        cart_item_info.quantity -= 1
        cart_item_info.save()
        return redirect('mycart')
    else:
        cart_item_info.delete()
        return redirect('mycart')


@login_required
def cart_success(request):
    cart_info = Cart.objects.filter(user=request.user)
    for items in cart_info:
        User_Info.objects.create(user=request.user, product_name=items.product, quantity=items.quantity  ,buy_time=datetime.datetime.now(),payment_satuts='success')
    Cart.objects.filter(user=request.user).delete()
    return redirect('myorder')


@login_required
def cart_failed(request):
    cart_info = Cart.objects.filter(user=request.user)
    for items in cart_info:
        User_Info.objects.create(user=request.user, product_name=items.product, quantity=items.quantity  ,buy_time=datetime.datetime.now(),payment_satuts='failed')
    Cart.objects.filter(user=request.user).delete()
    return redirect('myorder')


@login_required
def cart_remove(request,id):
    Cart.objects.filter(user=request.user,product_id=id).delete()
    # cart_info
    return redirect('/')
    
    
@login_required
def remove_quantity_home(request,id):
    try:
        cart_item_info = Cart.objects.get(id=id)
    except error.ObjectDoesNotExist: #to handle DoNotExist Error
        return redirect('/')
    if cart_item_info.quantity >1:
        cart_item_info.quantity -= 1
        cart_item_info.save()
        return redirect('/')
    else:
        cart_item_info.delete()
        return redirect('/')


@login_required
def add_quantity_home(request,id):
    try:
        cart_item_info = Cart.objects.get(id=id)
    except error.ObjectDoesNotExist: #to handle DoNotExist Error
        return redirect('/')
    cart_item_info.quantity += 1
    cart_item_info.save()
    return redirect('/')


def forget(request):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        user_input = request.POST.get('email')
        try:
            validate_email(user_input)
        except ValidationError as e:
            messages.info(request,'Enter Valid Email')
            return render(request,'newapp/forget_password.html', {'forget':'forget'})
        all_emails=User.objects.values_list('email')
        if (str(user_input),) in all_emails:
            user_info = User.objects.get(email=user_input)
            subject = 'OTP  For Reset Password'
            otp = ""
            for index in range(4):
                otp+=str(random.randint(1,9))
            try:
                Otp.objects.filter(user=user_info).delete()
                Otp.objects.create(user=user_info,otp=otp)
            except:
                Otp.objects.create(user=user_info,otp=otp)
            message = f'Hi {user_info.username}, here is your OTP {otp} for reset Password'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_info.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'newapp/forget_password.html',{'otp':'otp','id':user_info.id})
        else:
            messages.info(request,'Email not registered')
            return render(request,'newapp/forget_password.html',{'forget':'forget'})
    return render(request,'newapp/forget_password.html',{'forget':'forget'})


def forget_password(request,id):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        user_info = User.objects.get(pk=id)
        input_otp = request.POST.get('otp')
        otp_info = Otp.objects.filter(user=user_info).get()
        if otp_info.otp == input_otp:
            return render(request,'newapp/forget_password.html',{'data':'password','id':id})
            # return render(request,'newapp/change_password.html',{'id':id})
        else:
            messages.info(request,'Invalid Otp')
            return render(request,'newapp/forget_password.html',{'otp':'otp','id':id})
            # return render(request,'newapp/otp.html',{'id':id})
    
    return redirect('/forget')
    # return render(request,'newapp/otp.html',{'id':id})


def change_password(request,id):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        password_first = request.POST.get('password1')
        password_second = request.POST.get('password')
        if password_first == password_second:
            user = User.objects.get(pk=id)
            user.set_password(password_first)
            user.save()
            login(request,user=user)
            return redirect('/')
        else:
            messages.info(request,"Password Don't match")
            return render(request,'newapp/forget_password.html',{'data':'data','id':id})
    return redirect('/forget')