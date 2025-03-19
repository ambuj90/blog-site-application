from django.urls import path
from .views import download_site, domain_analysis_view

urlpatterns = [
    path("download/", download_site, name="download_site"),
    path("analyze/", domain_analysis_view, name="domain_analysis"),
]
