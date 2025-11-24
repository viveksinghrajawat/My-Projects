from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class product(models.Model):
    product_id = models.CharField(max_length = 120)
    product_img = models.CharField(max_length = 450, default="")
    product_name = models.CharField(max_length = 120)
    product_price = models.CharField(max_length = 120)
    def __str__(self):
        return self.product_name

class user_info(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product_name = models.ForeignKey(product,on_delete = models.CASCADE)
    buy_time = models.DateTimeField()
    payment_satuts = models.CharField(max_length = 120)