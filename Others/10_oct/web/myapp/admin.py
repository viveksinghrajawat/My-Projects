from . import models
from django.contrib import admin

# Register your models here.
@admin.register(models.quiz)
class Useradmin(admin.ModelAdmin):
    list_display=['question','ans']
    readonly_fields = ('ans',)
    def ans(self, question):
        ans=models.answer.objects.get(quest=question)
        return ans.right_ans

@admin.register(models.attempt)
class Useradmin(admin.ModelAdmin):
    list_display=['user','attempt_time']

@admin.register(models.user_info)
class Useradmin(admin.ModelAdmin):
    list_display=['answer']
    

@admin.register(models.answer)
class Useradmin(admin.ModelAdmin):
    list_display=['quest']