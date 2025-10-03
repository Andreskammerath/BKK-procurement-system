"""
URL configuration for users app.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Dashboard (main user view after login)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Note: Login/logout now handled by allauth at /accounts/login/ and /accounts/logout/
]

