from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Customer,
    Cart,
    Product,
    OrderPlaced,
    Contact,
    checkoutform,
    Price
)
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stripe_product_id', 'selling_price', 'stripe_price_id', 'discounted_price', 'description', 'brand', 'category', 'product_img', 'url']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['sno', 'name', 'email', 'phone', 'person', 'context']

@admin.register(checkoutform)
class CheckoutModelAdmin(admin.ModelAdmin):
    list_display = ['sno', 'name', 'email', 'phone', 'pmethod', 'context']

@admin.register(Price)
class PriceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'stripe_price_id', 'price']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']

def customer_info(self, obj):
    link = reverse("admin:app_customer_change", args=[obj.customer.pk])
    return format_html('<a href="{}">{}</a>', link, obj.customer.name)