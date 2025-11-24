from dataclasses import dataclass
from django.shortcuts import render
from django.contrib import messages
import django.core.exceptions as d
from . import models

# Create your views here.
def login(request):
    return render(request,'myapp/home.html')
def regis(request):
    if request.method == 'POST':
        l=[]
        l.append(request.POST.get("name"))
        l.append(request.POST.get("email"))
        data= models.reg.objects.all()
        flag=0
        for i in data:
            if i.email==l[0]:
                messages.info(request, 'username already present login')  
                return render(request,'myapp/home.html') 


        if request.POST.get("password")==request.POST.get("newpassword"):
            obj=models.reg(name=l[0],email=l[1],password=l[2])
            obj.save()
        else:
            messages.info(request, 'password not matched Incorrect!')  
            return render(request,'myapp/reg.html') 

    return render(request,'myapp/reg.html')

def check(request):
    try:
        if request.method == 'POST':
            try:
                em=request.POST.get("email")
                data= models.reg.objects.all()
                flag=0
                for i in data:
                    if i.email==em:
                        flag=1
                        pss=request.POST.get("password")
                        if i.password==pss:
                            return render(request,'myapp/log.html')
                        else:
                            messages.info(request, 'Your password is Incorrect!')  
                            return render(request,'myapp/home.html') 
                if flag!=0:
                    messages.info(request, 'Yerror!')
                    return render(request,'myapp/home.html')
            except d:
                messages.info(request, 'Yerror!')
                return render(request,'myapp/home.html')
            except ValueError:
                messages.info(request, 'Yerror!')
                return render(request,'myapp/home.html')
    except ValueError:
        return render(request,'myapp/home.html')
    return render(request,'myapp/home.html')