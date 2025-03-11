from django.db import models
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    content = models.TextField()
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='default.jpg')


    def __str__(self):
        return self.title

    def get_tags_list(self):
        """Convert tags from comma-separated string to a list."""
        return self.tags.split(",") if self.tags else []
