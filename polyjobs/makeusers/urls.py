from django.urls import path
from . import views
app_name = "makeusers"
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password_view, name="change_password"),
]
