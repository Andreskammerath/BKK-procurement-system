"""
Django-allauth adapter for custom Usuario model.
"""

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth to work with our Usuario model.
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Save a new user with email as the primary identifier.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Set default role for new users
        user.rol = 'VENDEDOR'  # Default role
        user.status = True
        user.is_active = True
        
        # If there's a logged-in user (admin creating account), track who created it
        if request.user.is_authenticated:
            user.created_by = request.user
            user.updated_by = request.user
        
        if commit:
            user.save()
        
        return user
    
    def get_login_redirect_url(self, request):
        """
        Redirect to dashboard after login.
        """
        return '/dashboard/'

