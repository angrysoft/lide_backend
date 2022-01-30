from django.contrib import admin
from .models import Positions, Locations, EmploymentType, Offers, Posts, Pages


class OffersAdmin(admin.ModelAdmin):
    list_filter = ("posted", )
    list_display = ("position", "edited", "posted")
    search_fields = ["position__name", "location__name", "employment_type__name", "details"]


class PostsAdmin(admin.ModelAdmin):
    list_filter = ("posted", )
    list_display = ("title", "edited", "posted")
    search_fields = ["title"]


admin.site.register(Offers, OffersAdmin)
admin.site.register(Positions)
admin.site.register(Locations)
admin.site.register(EmploymentType)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Pages)