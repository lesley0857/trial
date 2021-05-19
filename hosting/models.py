from django.db import models

# Create your models here.


class Products(models.Model):
    title  = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    description = models.TextField(null=True,blank=True)
    discount =  models.FloatField(blank=True,null=True)
    def __str__(self):
        return str(self.title)