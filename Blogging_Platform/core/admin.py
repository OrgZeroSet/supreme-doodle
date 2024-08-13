from django.contrib import admin
from .models import Posts

class PostsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "changes", "created_at"]
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Posts, PostsAdmin)