from django.db import models

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    content = models.TextField()
    image = models.FileField(upload_to="uploads/%Y/%m/%d/")
    changes = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]
