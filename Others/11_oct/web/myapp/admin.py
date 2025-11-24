from . import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Quiz_model)
class Useradmin(admin.ModelAdmin):
    list_display=['question','Right_answer']
    readonly_fields = ('Right_answer',)
    def Right_answer(self, question):
        answer=models.Answer_Model.objects.get(question=question)
        return answer.right_answer

@admin.register(models.User_Information)
class Useradmin(admin.ModelAdmin):
    list_display=['user','attempt_time']

@admin.register(models.Score_Calculator)
class Useradmin(admin.ModelAdmin):
    list_display=['question_id']   

@admin.register(models.Answer_Model)
class Useradmin(admin.ModelAdmin):
    list_display=['question']