from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'completed']
    inlines = [OrderItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description','image','category']
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
