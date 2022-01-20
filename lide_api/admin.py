from django.contrib import admin
from .models import Positions, Locations, EmploymentType, Offers, Posts

class OffersAdmin(admin.ModelAdmin):
    list_filter = ("posted", )
    list_display = ("position", "edited", "posted")
    search_fields = ["position__name", "location__name", "employment_type__name", "details"]


admin.site.register(Offers, OffersAdmin)
admin.site.register(Positions)
admin.site.register(Locations)
admin.site.register(EmploymentType)
admin.site.register(Posts)