from django.contrib import admin
from .models import Phone, Order


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'price_php', 'stock', 'is_available']
    list_filter = ['brand', 'is_available']
    search_fields = ['brand', 'model', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'quantity', 'total_price_php', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']

