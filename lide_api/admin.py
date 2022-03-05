from django.contrib import admin
from .models import Contacts


admin.site.site_header = "Lide Panel Administracyjny"
admin.site.register(Contacts)
