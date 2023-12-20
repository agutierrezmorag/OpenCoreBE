from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="query_results"),
    path("stats/", views.stats, name="stats"),
]
