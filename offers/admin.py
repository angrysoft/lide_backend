from django.contrib import admin
from .models import Offers, Positions, Locations, EmploymentType


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


admin.site.register(Offers, OffersAdmin)
admin.site.register(Positions)
admin.site.register(Locations)
admin.site.register(EmploymentType)