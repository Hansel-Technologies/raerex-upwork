from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'brand', 'model', 'price', 'available', 'requires_installation', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'brand', 'energy_efficiency', 'requires_installation']
    list_editable = ['price', 'available', 'requires_installation']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]