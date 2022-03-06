from django.contrib import admin
from .models import Posts


class PostsAdmin(admin.ModelAdmin):
    list_filter = ("posted",)
    list_display = ("title", "edited", "posted")
    search_fields = ["title"]


admin.site.register(Posts, PostsAdmin)
