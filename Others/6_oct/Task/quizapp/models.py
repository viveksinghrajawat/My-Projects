import datetime
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class quiz(models.Model):
    question= models.CharField(max_length=128)
    category= models.CharField(max_length=128)
    opt_1=models.CharField(max_length=120)
    opt_2=models.CharField(max_length=120)
    opt_3=models.CharField(max_length=120)
    opt_4=models.CharField(max_length=120)
    right_ans=models.CharField(max_length=120)
    time=models.CharField(max_length=120)

class user_info(models.Model):
    id_ques=models.IntegerField(default=0)
    answer=models.IntegerField(default=0)

class attempt(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    test_name=models.CharField(max_length=120)
    attempt_time=models.DateTimeField()
    score=models.CharField(max_length=120)