"""
URL configuration for procurement_system project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    
    # Authentication (allauth)
    path('accounts/', include('allauth.urls')),
    
    # Dashboard and custom views
    path('', include('users.urls')),
    
    # Redirect root to login
    path('', lambda request: redirect('account_login') if not request.user.is_authenticated else redirect('users:dashboard'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
