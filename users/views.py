"""
Views for user dashboard and management.
Note: Login/logout is now handled by django-allauth
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    """Main dashboard view."""
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)
