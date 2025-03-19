from django.shortcuts import render
from .models import Product

def filter_products_by_category(request, category_name):
    products = Product.objects.filter(category__iexact=category_name)  # Case-insensitive filter
    return render(request, 'products/product_list.html', {'products': products, 'category': category_name})



def all_products(request):
    products = Product.objects.all()[:3]  # ✅ Show only 3 products
    return render(request, 'products/all_products.html', {'products': products})