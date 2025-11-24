from .models import product, user_info
from django.contrib import admin

# Register your models here.
@admin.register(product)
class Useradmin(admin.ModelAdmin):
    list_display=['product_name','product_price']

@admin.register(user_info)
class Useradmin(admin.ModelAdmin):
    list_display=['user']
    readonly_fields=['user','product_name','buy_time','payment_satuts']