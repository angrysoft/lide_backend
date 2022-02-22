from django.contrib import admin
from .models import Contacts, Positions, Locations, EmploymentType, Offers, Posts, Pages


class OffersAdmin(admin.ModelAdmin):
    list_filter = ("posted",)
    list_display = ("position", "edited", "posted")
    search_fields = [
        "position__name",
        "location__name",
        "employment_type__name",
        "details",
    ]
    filter_horizontal = ("location", "employment_type")


class PostsAdmin(admin.ModelAdmin):
    list_filter = ("posted",)
    list_display = ("title", "edited", "posted")
    search_fields = ["title"]


admin.site.site_header = "Lide Panel Administracyjny"
admin.site.register(Offers, OffersAdmin)
admin.site.register(Positions)
admin.site.register(Locations)
admin.site.register(EmploymentType)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Pages)
admin.site.register(Contacts)
