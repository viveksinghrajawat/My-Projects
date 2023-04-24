import datetime,re
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product,User_Info,Cart
from django.core import exceptions as error
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def sign_in_page(request):
    if request.method == "POST":
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
    # import pdb;pdb.set_trace()
    try:
        product_info = Product.objects.get(pk=id)
    except: #to handle DoNotExist error
        return redirect('/')
    
    currency = 'INR'
    amount = (int(product_info.product_price) *100) # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'/paymenthandler/{id}'
    redirect_url = '/'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['redirect'] = redirect_url
    print(context['razorpay_amount'])
    # return render(request, 'index.html', context=context)
    return render(request, 'newapp/payment.html', context={'context':context, 'total':int(amount/100)})
    


@login_required
def cart_payment_page(request):
    try:
        cart_info = Cart.objects.filter(user=request.user)
        total_amount = 0
        for items in cart_info:
            total_amount += (int(float(items.product.product_price)) * items.quantity)
    except error.ObjectDoesNotExist: #to handle DoNotExist error
        return redirect('/')
    currency = 'INR'
    amount = total_amount*100  # Rs. 200
    print(amount)
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    # return render(request, 'index.html', context=context)
    return render(request, 'newapp/payment.html', context={'context':context})  


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


@csrf_exempt
def paymenthandler(request,id):
    # import pdb;pdb.set_trace()
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            product_info=Product.objects.get(pk=id)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = int(product_info.product_price)*100  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    product_info = Product.objects.get(pk=id)
                    User_Info.objects.create(user=request.user, product_name= product_info, buy_time=datetime.datetime.today(), payment_satuts='succesfull', order_id=razorpay_order_id, payment_id=payment_id)
                    # render success page on successful caputre of payment
                    user_data = User_Info.objects.filter(user=request.user).latest('id')
                    return render(request, 'newapp/success.html', {'data':user_data})
                except:
                    User_Info.objects.create(user=request.user, product_name= product_info, buy_time=datetime.datetime.today(), payment_satuts='failed', order_id=razorpay_order_id, payment_id=payment_id)
                    user_data = User_Info.objects.latest(user=request.user)
                    # if there is an error while capturing payment.
                    return render(request, 'newapp/failed.html', {'user_data':user_data})
            else:
 
                # if signature verification fails.
                User_Info.objects.create(user=request.user, product_name= product_info, buy_time=datetime.datetime.today(), payment_satuts='failed', order_id=razorpay_order_id, payment_id=payment_id)
                user_data = User_Info.objects.latest(user=request.user)
                return render(request, 'newapp/failed.html', {'user_data':user_data})
                # return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return  redirect('/')
    else:
       # if other than POST request is made.
        return redirect('/')