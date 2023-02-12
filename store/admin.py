from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_available')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
