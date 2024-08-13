from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<slug:article_slug>/<int:article_id>", views.article, name="article"),
]