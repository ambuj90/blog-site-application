from django.urls import path
from .views import download_site

urlpatterns = [
    path("download/", download_site, name="download_site"),
]
