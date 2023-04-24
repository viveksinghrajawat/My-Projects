from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Quiz_model(models.Model):
    question= models.CharField(max_length=128)
    option_1=models.CharField(max_length=120,default="")
    option_2=models.CharField(max_length=120,default="")
    option_3=models.CharField(max_length=120,default="")
    option_4=models.CharField(max_length=120,default="")
    def __str__(self):
        return self.question

class Answer_Model(models.Model):
    question=models.OneToOneField(Quiz_model,on_delete=models.CASCADE)
    right_answer=models.CharField(max_length=120)
    question_time=models.CharField(max_length=120)

class Score_Calculator(models.Model):
    question_id=models.IntegerField(default=0)
    marks_user=models.IntegerField(default=0)

class User_Information(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attempt_time=models.DateTimeField()
    score=models.CharField(max_length=120)