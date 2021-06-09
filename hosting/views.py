from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404,get_list_or_404,_get_queryset
from django.http import Http404,request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils import timezone
from .decorator import *
# Create your views here.


def product_view(request):
    productlist = Products.objects.all()
    context = {'productlist': productlist, }
    return render(request, 'product.html', context)


def product_detail_view(request,id):
    product_detail = Products.objects.get(id = id)
    context = {'product_detail':product_detail}
    return render(request,"product-detail.html",context)


@login_required(login_url='login')
def Checkout(request):
    if request.method == "POST":
        print(request.POST)
    form = Checkoutform(request.POST )
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False, )
    if order_qs:
        billing_address = Checkoutt.objects.filter(user=request.user)
        if billing_address:
            print('bill exixts')


        else:
            form = Checkoutform(request.POST)
            if form.is_valid():
                email = request.user.email
                Address = form.cleaned_data.get('Address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                Zip = form.cleaned_data.get('Zip')
                payment_options = form.cleaned_data.get('payment_options')
                billing_address = Checkoutt.objects.create(user=request.user,
                                                              Email=email,
                                                              Address=Address,
                                                              Country=country,
                                                              state=state,
                                                              Zip=Zip,
                                                              Payment_options=payment_options,
                                                              )
                billing_address.save()
                print(billing_address)
                a = Order.objects.get(user=request.user,
                                        ordered=False,
                                      )
                a.Billing_address = billing_address
                print(a.Billing_address)
                a.save()

            else:
                print('not valid')
    else:
        messages.error(request,'you dont have an order')
    context = {'form': form}
    return render(request, 'checkout.html', context)


@authenticate_user
def signup_view(request,**kwargs):
    form = createuserform()
    if request.method == "POST":
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            user = form.save()
           # print(user.username)
            #Customer.objects.create(name=user.username,user = user,email=user.email)  # with this method the Customer name wont change if the User's name is updated  it is better to use django signals
           # print(user)

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name="Customers")  #Group is the user group in the admin
            user.groups.add(group)    #add form.save to a group named customer
            messages.success(request,'signup successful'+ " " + username)# it is stored as a value  no need to assign a  value to the messages. no need to pass it through context
            Customer.objects.create(user=user, name=user.username)
            return redirect('login')
    #a = form.errors
    context = {'form':form}
    return render(request,'signup.html',context)

@authenticate_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:  # not none    means the user name is there in database                login(request, username)

            login(request, user)
            return redirect('customer',request.user.customer.id)
        else:
            messages.info(request, "Username OR Password is incorrect")  # you dont need to pass through context
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def customer_view(request,id):
    customer = Customer.objects.get(id=id)
    print(customer.name)
    productlist = Products.objects.all()
    context = {'productlist': productlist,"customer":customer}
    return render(request, 'customer.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def all_orders(request):
    global orders
    orders = Order.objects.all


    context  = {"orders":orders}
    return render(request, 'allorders.html', context)

def order_detail(request,id):
    order = Order.objects.get(id=id)
    j = OrderItem.objects.filter(order=order)

    context = {"j": j,"order":order}
    return render(request, 'orderdetail.html', context)

# decorator for only admin
def order_summary(request):
    o = OrderItem.objects.filter(user=request.user)

    x = []
    z = []

    a = int()
    b = int()
    for i in o:
        v = i.realprice()
        x.append(v)
        print(x)
        a = sum(x)
        print(a)
    for c in o:
        j = c.saved_price()
        z.append(j)
        print(z)
        b = sum(z)
        print(b)

    context = {'o':o,"a":a,"b":b}
    return render(request, 'ordersummary.html', context)


def order_summary_for_Anonymous(request):

    context = {}
    return render(request, 'ordersummary.html', context)

def add_to_cart(request,id):
    # declaring Queryset
    product = get_object_or_404(Products,id=id)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False )
    orderitem_qs = OrderItem.objects.filter(user=request.user,
                                    ordered=False,
                                    item=product.id
                                 )
    #check to see iff there iss an Orderqueryset
    if order_qs:
        order = order_qs[0] # this specifies it is the first queryset
        if orderitem_qs: # check for orderitem queryset

            orderitem_qs = OrderItem.objects.get(user=request.user,
                                            ordered=False,
                                            item=product.id)

            orderitem_qs.quantity = orderitem_qs.quantity + 1
            orderitem_qs.save()
        else:
            messages.info(request,'item will be added to cart.')
            j = Order.objects.get(user=request.user,
                                  ordered=False,
                                  )
            OrderItem.objects.create(user=request.user,
                                     ordered=False,
                                     item_id=product.id,
                                    order=j,
                                     quantity=1)
            OrderItem.save
    else:
        Order.objects.create(user=request.user,
                              ordered=False,
                              ordered_date= timezone.now()
                              )
        Order.save
        j = Order.objects.get(user=request.user,
                                 ordered=False,

                                 )
        OrderItem.objects.create(user=request.user,
                                 ordered=False,
                                 item_id=product.id,
                                 quantity=1,
                                 order=j)
        OrderItem.save



    return redirect('customer',request.user.customer.id)




