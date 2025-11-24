from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    product_id = models.CharField(max_length = 120)
    product_img = models.CharField(max_length = 450, default="")
    product_name = models.CharField(max_length = 120)
    product_price = models.CharField(max_length = 120)
    def __str__(self):
        return self.product_name

class Order(models.Model):
    email = models.EmailField(max_length=254)
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email