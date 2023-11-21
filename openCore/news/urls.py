from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.news_detail, name='news_detail')
]
