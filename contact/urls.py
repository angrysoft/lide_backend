from django.urls import path
from contact import views

urlpatterns = [path("", views.MailView.as_view(), name="mail")]
