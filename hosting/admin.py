from django.contrib import admin

# Register your models here.
from hosting.models import *
admin.site.register(Checkoutt),
admin.site.register(Products),
admin.site.register(Customer),
admin.site.register(Order),
admin.site.register(OrderItem),

