from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from django.contrib.auth.forms import UserCreationForm
from .models import *

class createuserform(UserCreationForm): #for registering a user

    class Meta:
        model = User
        fields = ['username','email','password1','password2']



PAYMENT_CHOICES = (('S','Stripe'),('P','Paypal'))

class Checkoutform(forms.Form):

    Street_address = forms.CharField(widget=forms.TextInput(attrs=
                                  {'placeholder':'1234 july str.'}))

    Apartment = forms.CharField(required=False, widget=forms.TextInput
                                (attrs={'placeholder':'apartment or suite'}))

    Address = forms.CharField(widget=forms.TextInput(
                             attrs={'class': 'form-control'}))

    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget())


    state = forms.ChoiceField(required=False)

    Zip = forms.CharField(widget=forms.TextInput(
                              attrs={'class': 'form-control'}))


    payment_options = forms.ChoiceField(widget=forms.RadioSelect,
                                        choices=PAYMENT_CHOICES)
