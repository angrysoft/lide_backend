from django.urls import path
from contact import views

urlpattern = [
    path("", views.MailView.as_view())
]
