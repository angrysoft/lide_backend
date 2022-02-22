from django.urls import include, path, re_path

from lide_api import views


urlpatterns = [
    path("offers", views.OffersListView.as_view()),
    path("offer/<int:offer_id>", views.OfferDetails.as_view()),
    path("offers/search", views.OfferSearch.as_view()),
    path("posts/", views.PostsListView.as_view()),
    path("post/<int:post_id>", views.PostDetails.as_view()),
    path("page/<slug:slug>", views.Page.as_view()),
    path("contacts", views.ContactsView.as_view()),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
]
