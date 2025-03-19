from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    list_per_page = 10  # ✅ Pagination in admin
    fields = ('name', 'category', 'price', 'description', 'image')  # ✅ Allows image upload
