from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:pk>/', views.news_detail, name='news_detail'),
    path('search/', views.search, name='query_results'),
]
