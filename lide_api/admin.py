from django.contrib import admin
from .models import Positions, Locations, EmploymentType, Offers, Posts

admin.site.register(Positions)
admin.site.register(Locations)
admin.site.register(EmploymentType)
admin.site.register(Offers)
admin.site.register(Posts)