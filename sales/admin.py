from django.contrib import admin
from .models import Seller
# Register your models here.

@admin.register(Seller)
class SellerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone', 'email', 'state', 'stage_of_business', 'company_name', 'company_size', 'company_address', 'city', 'zipcode', 'state', 'gst']

