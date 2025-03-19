from django.urls import path
from .views import filter_products_by_category, all_products

urlpatterns = [
    path("", all_products, name="all_products"),  # ✅ This handles /products/
    path("<str:category_name>/", filter_products_by_category, name="filter_products_by_category"),
]
