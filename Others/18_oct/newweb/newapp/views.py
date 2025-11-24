import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Product 


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
    success_url=YOUR_DOMAIN + '/success',
    cancel_url=YOUR_DOMAIN + '/cancel',
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
	 #NEW CODE
        session = event['data']['object']
        # print(session)
        #getting information of order from session
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        sessionID = session["id"]
				#grabbing id of the order created 
        ID=session["metadata"]["product_id"]
        user_id=session["metadata"]["user_id"]
        # ID=session["metadata"]["order_id"]
				 #Updating order
        product_info = Product.objects.get(pk=ID)
        user_info = User.objects.get(pk=user_id)
        # print(user_info)
        Order.objects.create(user=user_info, product=product_info, email=customer_email, amount=price, paid=True, description=sessionID)
        # Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)

    return HttpResponse(status=200)

#success view
def success(request):
    return render(request,'newapp/success.html')
    
#cancel view
def cancel(request):
    return render(request,'newapp/cancel.html')


def sign_in_page(request):
    if request.method == "POST":
        input_user_name = request.POST.get("username")
        input_password = request.POST.get("password")
        # import pdb;pdb.set_trace()
        user_valid = authenticate(request, username = input_user_name, password = input_password)
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
def my_orders(request):
    order_data=Order.objects.filter(user=request.user)
    return render(request, 'newapp/my_order.html', context={'orderdata':order_data })


def home_page(request):
    # request.session.flush()
    product_data=Product.objects.all()
    return render(request, 'newapp/home_page.html', context={'product_data':product_data })