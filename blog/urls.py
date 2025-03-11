from django.urls import path
from .views import home, post_detail,testing

urlpatterns = [
    path("", home, name="home"),
    path("post/<int:post_id>/", post_detail, name="post_detail"),
    path("testing/", testing, name="testing"),
]
