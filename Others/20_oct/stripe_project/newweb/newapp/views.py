import datetime,re
import string
import random
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product,Cart
from django.core import exceptions as error
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order 

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
def my_orders(request):
    order_data = Order.objects.filter(user=request.user)
    return render(request, 'newapp/my_order.html', context={'orderdata':order_data })



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


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'


@csrf_exempt
def create_checkout_session(request,pk):
    #Updated- creating Order object
    # print(request.user)
    product_info = Product.objects.get(pk=pk)
    # order = Order(user=request.user, product=product_info, email=" ", paid="False", amount=product_info.product_price, description=" ")
    # order.save()
    session = stripe.checkout.Session.create(
    client_reference_id = request.user.id if request.user.is_authenticated else None,
    payment_method_types = ['card'],
    line_items = [{
      'price_data': {
        'currency': 'inr',
        'product_data': {
          'name': product_info.product_name,
        },
        'unit_amount': int(float(product_info.product_price) * 100), #to handle
      },
      'quantity': 1,
    }],
   #Update - passing order ID in checkout to update the order object in webhook
    metadata={ 
        # "order_id":order.id
        "user_id":request.user.id,
        "product_id":product_info.id
    },
    mode='payment',
    success_url=YOUR_DOMAIN + '/myorder',
    cancel_url=YOUR_DOMAIN + '/',
    )
    return JsonResponse({'id': session.id})


@csrf_exempt
def create_checkout_session_cart(request):
    #Updated- creating Order object
    # print(request.user)
    try:
        cart_info = Cart.objects.filter(user=request.user)
        total_amount = 0
        for items in cart_info:
            total_amount += (int(float(items.product.product_price)) * items.quantity)
    except error.ObjectDoesNotExist: #to handle DoNotExist error
        return redirect('/')
    # order = Order(user=request.user, product=product_info, email=" ", paid="False", amount=product_info.product_price, description=" ")
    # order.save()
    session = stripe.checkout.Session.create(
    client_reference_id = request.user.id if request.user.is_authenticated else None,
    payment_method_types = ['card'],
    line_items = [{
      'price_data': {
        'currency': 'inr',
        'product_data': {
          'name': 'cart',
        },
        'unit_amount': total_amount *100, #to handle
      },
      'quantity': 1,
    }],
   #Update - passing order ID in checkout to update the order object in webhook
    metadata={ 
        # "order_id":order.id
        "product_id": 0,
        "user_id":request.user.id,
    },
    mode='payment',
    success_url=YOUR_DOMAIN + '/myorder',
    cancel_url=YOUR_DOMAIN + '/',
    )
    return JsonResponse({'id': session.id})



@csrf_exempt
def webhook(request):
    # print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        #getting information of order from session
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        orderid = session["payment_intent"]
        # sessionID = session["id"]
		#grabbing id of the order created 
        ID=session["metadata"]["product_id"]
        user_id=session["metadata"]["user_id"]
        user_info = User.objects.get(pk=user_id)
        # res = ''.join(random.choices(string.ascii_uppercase +
        #                      string.digits,k=5))
        if ID != '0':
            product_info = Product.objects.get(pk=ID)
            Order.objects.create(user=user_info, product=product_info, email=customer_email ,amount=product_info.product_price, buy_time=datetime.datetime.now(), order_id=orderid, payment_satuts= 'success')
        else:
            cart_info = Cart.objects.filter(user=user_info)
            for items in cart_info:
               Order.objects.create(user=user_info, product=items.product, email=customer_email ,quantity=items.quantity , amount=items.product.product_price, buy_time=datetime.datetime.now(), order_id=orderid, payment_satuts= 'success')
            cart_info.delete()
    return HttpResponse(status=200)