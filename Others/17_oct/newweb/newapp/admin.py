from .models import Cart, Product,User_Info
from django.contrib import admin

# Register your models here.
# @admin.register(Product)
# class Useradmin(admin.ModelAdmin):
#     list_display=['product_name','product_price']


@admin.register(User_Info)
class Useradmin(admin.ModelAdmin):
    list_display=['user']
    readonly_fields=['user','product_name','buy_time','payment_satuts']

admin.site.register(Product)

@admin.register(Cart)
class Useradmin(admin.ModelAdmin):
    list_display=['product']
