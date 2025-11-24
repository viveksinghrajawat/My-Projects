from .models import Cart, Product,Order
from django.contrib import admin

# Register your models here.
@admin.register(Product)
class Useradmin(admin.ModelAdmin):
    list_display=['product_name','product_price']


@admin.register(Cart)
class Useradmin(admin.ModelAdmin):
    list_display=['product']

admin.site.register(Order)