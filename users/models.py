"""
User models for the procurement system.
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class RolUsuario(models.TextChoices):
    """User role enumeration."""
    VENDEDOR = 'VENDEDOR', 'Vendedor'
    COMPRADOR = 'COMPRADOR', 'Comprador'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    SUPERVISOR = 'SUPERVISOR', 'Supervisor'


class UsuarioManager(BaseUserManager):
    """Custom manager for Usuario model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', RolUsuario.ADMINISTRADOR)
        extra_fields.setdefault('status', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    """
    Custom user model using email as the unique identifier.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Email', max_length=255, unique=True)
    rol = models.CharField(
        'Rol',
        max_length=20,
        choices=RolUsuario.choices,
        default=RolUsuario.VENDEDOR
    )
    status = models.BooleanField('Activo', default=True)
    
    # Required for Django admin
    is_staff = models.BooleanField('Staff', default=False)
    is_active = models.BooleanField('Activo', default=True)
    
    # Audit fields
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_creados',
        verbose_name='Creado por'
    )
    updated_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_actualizados',
        verbose_name='Actualizado por'
    )
    deleted_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_eliminados',
        verbose_name='Eliminado por'
    )
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='idx_usuarios_email'),
            models.Index(fields=['rol'], name='idx_usuarios_rol'),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the email as the full name."""
        return self.email
    
    def get_short_name(self):
        """Return the email as the short name."""
        return self.email
