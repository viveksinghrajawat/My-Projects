import datetime
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class quiz(models.Model):
    question= models.CharField(max_length=128)
    opt_1=models.CharField(max_length=120,default="")
    opt_2=models.CharField(max_length=120,default="")
    opt_3=models.CharField(max_length=120,default="")
    opt_4=models.CharField(max_length=120,default="")
    def __str__(self):
        return self.question

class answer(models.Model):
    quest=models.OneToOneField(quiz,on_delete=models.CASCADE)
    right_ans=models.CharField(max_length=120)
    time=models.CharField(max_length=120)

class user_info(models.Model):
    id_ques=models.IntegerField(default=0)
    answer=models.IntegerField(default=0)

class attempt(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attempt_time=models.DateTimeField()
    score=models.CharField(max_length=120)