from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("lide_api.urls")),
    path("api/mail", include("contact.urls")),
]
