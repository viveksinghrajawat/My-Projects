from wsgiref import validate
from django.db import models
# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    #validate(email)
    password=models.CharField(max_length=20)
    
    #validate(password)