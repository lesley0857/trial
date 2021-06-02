from django.db import models
from django.urls import reverse

# Create your models here.





class Products(models.Model):
    TAGS = (('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Beauty','Beauty'))
    title  = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    description = models.TextField(null=True,blank=True)
    discount =  models.FloatField(blank=True,null=True)
    tag = models.CharField(max_length=200,choices=TAGS,default= 'TAGS[0]')
    profile_pic = models.ImageField(blank=True)
    def __str__(self):
        return str(self.title)



    def get_absolute_url(self):
        return reverse('productdetail',kwargs={"id":self.id})