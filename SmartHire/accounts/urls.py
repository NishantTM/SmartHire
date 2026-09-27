from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/', views.login_view, name='login'),
    path('register/', views.logout_view, name='logout'),
]
