from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.http import Http404,request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required(login_url='login')
def product_view(request):
    productlist = Products.objects.all()
    context = {'productlist': productlist, }
    return render(request, 'product.html', context)


def product_detail_view(request,id):
    product_detail = Products.objects.get(id = id)
    context = {'product_detail':product_detail}
    return render(request,"product-detail.html",context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:  # not none    means the user name is there in database                login(request, username)

            login(request, user)
            return redirect("products")
        else:
            messages.info(request, "Username OR Password is incorrect")  # you dont need to pass through context
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
