from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.book_list, name="home"),
    path("about/", views.about, name="about"),
    path("home/", views.home_redirect, name="home_redirect"),
    path("template-demo/", views.template_demo, name="template_demo"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
    path("artists/profile/<slug:slug>/", views.artist_profile, name="artist_profile"),
    path("artists/<int:pk>/", views.artist_detail, name="artist_detail"),
    path("books/search/<slug:slug>/", views.book_search, name="book_search"),
    path("users/<int:user_id>/", views.user_profile, name="user_profile"),
    re_path(r"^digits/(?P<digits>\d+)/$", views.digits_only, name="digits_only"),
]
