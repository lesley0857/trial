from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User

# Create your models here.


class Checkoutt(models.Model):
    user = models.ForeignKey(User,null = True,on_delete = models.CASCADE,default=True)
    Email = models.EmailField()
    Address = models.CharField(max_length=200,null=True)

    Country = CountryField(multiple=False)
    state = models.CharField(max_length=200, null=True,blank=False)
    Zip = models.CharField(max_length=200, null=True)
    Payment_options = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.user.username

    def paymenturl(self):
        return reverse('payment', kwargs={"id": self.Payment_options})


class Customer(models.Model):
    PLANS = (('Diamond','Diamond'),('Gold','Gold'),('Silver','Silver'))
    user = models.OneToOneField(User,null = True,on_delete = models.CASCADE,default=True)
    name  = models.CharField(null=True,max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    created = models.DateTimeField(null=True,auto_now=False,auto_now_add=True)
    plans = models.CharField(max_length=200,choices=PLANS,default= 'PLANS[0]')
    profile_pic = models.ImageField(default="/Koala.jpg/")

    def __str__(self):
        return str(self.user)



    def get_absolute_url(self):
        return reverse('customer')


class Products(models.Model):
    TAGS = (
        ('Indoor', 'Indoor'),
            ('Outdoor', 'Outdoor'),
            ('Beauty','Beauty')
            )
    title  = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    description = models.TextField(null=True,blank=True)
    discount =  models.FloatField(blank=True,null=True)
    tag = models.CharField(max_length=200,choices=TAGS,default= 'TAGS[0]')
    profile_pic = models.ImageField(blank=True)
    def __str__(self):
        return str(self.title)

    def add_to_cart_url(self):
        return reverse('addtocart',kwargs={"id":self.id})

    def get_absolute_url(self):
        return reverse('productdetail',kwargs={"id":self.id})



class Order(models.Model):
    STATUS = (('delivered','delivered'),('pending','pending'),('out for delivery','out for delivery'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    Billing_address = models.ForeignKey(Checkoutt, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Products,null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True,default='0')
    ordered = models.BooleanField(default=False)
    order = models.ForeignKey(Order,null=True,on_delete=models.SET_NULL)


    def __str__(self):
        return str(str(self.user) + ' ' + str(self.item))


    def realprice(self):
        if self.item.discount:
            j =self.item.price - self.item.discount
            return j * self.quantity
        return self.item.price * self.quantity

    def saved_price(self):
        if self.item.discount:
            total_discount = self.item.discount * self.quantity
            return total_discount
        return self.realprice()