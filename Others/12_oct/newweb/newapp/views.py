from django.shortcuts import redirect, render

def success_page(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,'newapp/success.html')
  
def home_page(request):
    return render(request,'newapp/home_page.html')