from django.contrib import admin
from .models import Order,Product

# Register your models here.

admin.site.register(Order)

@admin.register(Product)
class Useradmin(admin.ModelAdmin):
    list_display=['product_name','product_price']