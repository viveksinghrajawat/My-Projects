from django.contrib import admin
from .models import Order,product

# Register your models here.

admin.site.register(Order)

@admin.register(product)
class Useradmin(admin.ModelAdmin):
    list_display=['product_name','product_price']