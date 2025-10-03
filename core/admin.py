"""
Admin configuration for core models.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Proveedor, Cliente, FormaDeEntrega, Articulo, Despachante,
    ProveedorFormaEntrega
)


@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    """Admin interface for Proveedor model."""
    
    list_display = ['razon_social', 'cuit', 'status', 'es_proveedor_nacional', 'created_at']
    list_filter = ['status', 'es_proveedor_nacional', 'created_at']
    search_fields = ['razon_social', 'cuit', 'localizacion']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('razon_social', 'cuit', 'localizacion')
        }),
        ('Estado', {
            'fields': ('status', 'es_proveedor_nacional')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    """Admin interface for Cliente model."""
    
    list_display = ['razon_social', 'cuit', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['razon_social', 'cuit', 'email', 'contact_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('razon_social', 'cuit', 'localizacion')
        }),
        ('Información de Contacto', {
            'fields': ('web_page', 'phone_number', 'email')
        }),
        ('Contacto Principal', {
            'fields': ('contact_name', 'contact_phone', 'contact_email')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Articulo)
class ArticuloAdmin(ImportExportModelAdmin):
    """Admin interface for Articulo model."""
    
    list_display = ['descripcion', 'marca', 'modelo', 'familia', 'status', 'created_at']
    list_filter = ['status', 'familia', 'marca', 'nivel_uso', 'created_at']
    search_fields = ['descripcion', 'marca', 'modelo', 'codigo_fabricante', 'palabras_claves', 'tags']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('descripcion', 'marca', 'modelo', 'tipo', 'codigo_fabricante')
        }),
        ('Clasificación', {
            'fields': ('familia', 'sub_familia', 'categoria_lvl1', 'categoria_lvl2', 
                      'categoria_lvl3', 'categoria_lvl4', 'industria', 'nivel_uso')
        }),
        ('Materiales', {
            'fields': ('material_principal', 'material_secundario')
        }),
        ('Dimensiones', {
            'fields': ('peso_valor', 'peso_unidad', 'largo_valor', 'largo_unidad',
                      'alto_valor', 'alto_unidad', 'ancho_valor', 'ancho_unidad')
        }),
        ('Metadata', {
            'fields': ('palabras_claves', 'tags', 'especificacion_tecnica')
        }),
        ('URLs', {
            'fields': ('url_ficha_tecnica', 'url_manual_tecnico', 'url_imagen_principal')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FormaDeEntrega)
class FormaDeEntregaAdmin(admin.ModelAdmin):
    """Admin interface for FormaDeEntrega model."""
    
    list_display = ['nombre', 'descripcion', 'created_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(Despachante)
class DespachanteAdmin(ImportExportModelAdmin):
    """Admin interface for Despachante model."""
    
    list_display = ['razon_social', 'cuit', 'email', 'telefono', 'created_at']
    search_fields = ['razon_social', 'cuit', 'email', 'contact_name']
    ordering = ['razon_social']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('razon_social', 'cuit', 'direccion')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'telefono_secundario', 'email', 'email_secundario', 'contact_name')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProveedorFormaEntrega)
class ProveedorFormaEntregaAdmin(admin.ModelAdmin):
    """Admin interface for ProveedorFormaEntrega junction model."""
    
    list_display = ['proveedor', 'forma_entrega', 'created_at']
    list_filter = ['created_at']
    search_fields = ['proveedor__razon_social', 'forma_entrega__nombre']
