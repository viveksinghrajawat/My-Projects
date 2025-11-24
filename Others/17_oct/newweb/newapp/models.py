from django.contrib.auth.models import User
from django.db import models
from django_mysql.models import ListCharField
import json
# Create your models here.
class Product(models.Model):
    product_catagory = models.CharField(max_length = 120)
    product_img = models.CharField(max_length = 450, default="")
    product_name = models.CharField(max_length = 120)
    product_price = models.CharField(max_length = 120)
    foo = models.CharField(max_length=200 ,default="" )

    # def  __str__(self) :
    #     return self.product_img

    def set_foo(self, x):
        self.foo = json.dumps(x)

    def get_foo(self):
        return json.loads(self.foo)
    
    def __str__(self):
        return self.product_name

class User_Info(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product_name = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity=models.IntegerField(default=1)
    buy_time = models.DateTimeField()
    payment_satuts = models.CharField(max_length = 120)
    def  __str__(self) :
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    def  __str__(self) :
        return self.product.product_name
    

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    otp =  models.CharField(max_length = 120)