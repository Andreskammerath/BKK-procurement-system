"""
Admin configuration for user models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Admin interface for Usuario model."""
    
    list_display = ['email', 'rol', 'status', 'is_staff', 'created_at']
    list_filter = ['rol', 'status', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información del Usuario'), {'fields': ('rol', 'status')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Auditoría'), {'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'rol', 'status', 'is_staff'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Override save to track who created/updated the user."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
