from django.urls import path
from . import views
app_name = "scraper"
urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('jobs/<int:pk>/favorite-toggle/', views.favorite_toggle, name='favorite_toggle'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    ]