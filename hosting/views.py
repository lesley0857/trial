from django.shortcuts import render
from .models import *
# Create your views here.
def product_view(request):
    productlist = Products.objects.all()
    context = {'productlist': productlist, }
    return render(request, 'product.html', context)