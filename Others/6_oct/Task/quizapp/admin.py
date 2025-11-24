from . import models
from django.contrib import admin

# Register your models here.
@admin.register(models.quiz)
class Useradmin(admin.ModelAdmin):
    list_display=['question','category']

@admin.register(models.attempt)
class Useradmin(admin.ModelAdmin):
    list_display=['user','attempt_time']

@admin.register(models.user_info)
class Useradmin(admin.ModelAdmin):
    list_display=['answer']