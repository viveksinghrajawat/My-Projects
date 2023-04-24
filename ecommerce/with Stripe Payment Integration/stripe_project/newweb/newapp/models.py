import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    product_catagory = models.CharField(max_length = 120)
    product_img = models.CharField(max_length = 450, default="")
    product_name = models.CharField(max_length = 120)
    product_price = models.CharField(max_length = 120)
    def __str__(self):
        return self.product_name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    quantity=models.IntegerField(default=1)
    buy_time = models.DateTimeField()
    payment_satuts = models.CharField(max_length = 120)
    amount = models.IntegerField()
    order_id = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email