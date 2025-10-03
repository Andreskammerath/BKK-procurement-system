"""
Admin configuration for procurement models.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Solped, DetalleSolped, PedidoDeCotizacion, PedidoCotizacionProveedor,
    DetallePedidoCotizacionProveedor, CotizacionProveedor, DetalleCotizacionProveedor,
    Cotizacion, OrdenCompraProveedor, DetalleOrdenCompraProveedor,
    OrdenCompraCliente, DetalleOrdenCompraCliente, Remito, DetalleRemito,
    Envio, Comunicacion, Actividad, PedidoCotizacionSolped, CotizacionSolped,
    CotizacionGanador
)


class DetalleSolpedInline(admin.TabularInline):
    """Inline for Solped details."""
    model = DetalleSolped
    extra = 1
    fields = ['articulo', 'cantidad_valor', 'cantidad_unidad']


@admin.register(Solped)
class SolpedAdmin(ImportExportModelAdmin):
    """Admin interface for Solped model."""
    
    list_display = ['nro_solped', 'status', 'created_at', 'created_by']
    list_filter = ['status', 'created_at']
    search_fields = ['nro_solped']
    ordering = ['-created_at']
    inlines = [DetalleSolpedInline]
    
    fieldsets = (
        ('Información', {
            'fields': ('nro_solped', 'status')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PedidoDeCotizacion)
class PedidoDeCotizacionAdmin(admin.ModelAdmin):
    """Admin interface for PedidoDeCotizacion model."""
    
    list_display = ['id', 'cliente', 'status', 'fecha_vencimiento', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_vencimiento']
    search_fields = ['cliente__razon_social']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


class DetallePedidoCotizacionProveedorInline(admin.TabularInline):
    """Inline for quote request details."""
    model = DetallePedidoCotizacionProveedor
    extra = 1


@admin.register(PedidoCotizacionProveedor)
class PedidoCotizacionProveedorAdmin(admin.ModelAdmin):
    """Admin interface for PedidoCotizacionProveedor model."""
    
    list_display = ['id', 'proveedor', 'status', 'fecha_vencimiento', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_vencimiento']
    search_fields = ['proveedor__razon_social']
    ordering = ['-created_at']
    inlines = [DetallePedidoCotizacionProveedorInline]


class DetalleCotizacionProveedorInline(admin.TabularInline):
    """Inline for supplier quotation details."""
    model = DetalleCotizacionProveedor
    extra = 1
    fields = ['articulo', 'cantidad_valor', 'cantidad_unidad', 'precio_unitario_valor', 'precio_unitario_moneda']


@admin.register(CotizacionProveedor)
class CotizacionProveedorAdmin(ImportExportModelAdmin):
    """Admin interface for CotizacionProveedor model."""
    
    list_display = ['id', 'proveedor', 'status', 'fecha_vencimiento', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_vencimiento']
    search_fields = ['proveedor__razon_social']
    ordering = ['-created_at']
    inlines = [DetalleCotizacionProveedorInline]
    date_hierarchy = 'created_at'


@admin.register(Cotizacion)
class CotizacionAdmin(ImportExportModelAdmin):
    """Admin interface for Cotizacion model."""
    
    list_display = ['id', 'cliente', 'status', 'margen', 'fecha_vencimiento', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_vencimiento']
    search_fields = ['cliente__razon_social']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


class DetalleOrdenCompraProveedorInline(admin.TabularInline):
    """Inline for purchase order details."""
    model = DetalleOrdenCompraProveedor
    extra = 1
    fields = ['articulo', 'cantidad_valor', 'cantidad_unidad', 'precio_unitario_valor', 'precio_unitario_moneda']


@admin.register(OrdenCompraProveedor)
class OrdenCompraProveedorAdmin(ImportExportModelAdmin):
    """Admin interface for OrdenCompraProveedor model."""
    
    list_display = ['numero_orden', 'proveedor', 'status', 'fecha_entrega_estimada', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_entrega_estimada']
    search_fields = ['numero_orden', 'proveedor__razon_social']
    ordering = ['-created_at']
    inlines = [DetalleOrdenCompraProveedorInline]
    date_hierarchy = 'created_at'


class DetalleOrdenCompraClienteInline(admin.TabularInline):
    """Inline for sales order details."""
    model = DetalleOrdenCompraCliente
    extra = 1
    fields = ['articulo', 'cantidad_valor', 'cantidad_unidad', 'precio_valor', 'precio_moneda']


@admin.register(OrdenCompraCliente)
class OrdenCompraClienteAdmin(ImportExportModelAdmin):
    """Admin interface for OrdenCompraCliente model."""
    
    list_display = ['numero_orden', 'cliente', 'status', 'fecha_entrega_estimada', 'created_at']
    list_filter = ['status', 'created_at', 'fecha_entrega_estimada']
    search_fields = ['numero_orden', 'cliente__razon_social']
    ordering = ['-created_at']
    inlines = [DetalleOrdenCompraClienteInline]
    date_hierarchy = 'created_at'


class DetalleRemitoInline(admin.TabularInline):
    """Inline for delivery receipt details."""
    model = DetalleRemito
    extra = 1


@admin.register(Remito)
class RemitoAdmin(ImportExportModelAdmin):
    """Admin interface for Remito model."""
    
    list_display = ['numero_remito', 'destinatario', 'status', 'fecha_envio', 'created_at']
    list_filter = ['status', 'fecha_envio', 'created_at']
    search_fields = ['numero_remito', 'destinatario__razon_social']
    ordering = ['-created_at']
    inlines = [DetalleRemitoInline]


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    """Admin interface for Envio model."""
    
    list_display = ['numero_seguimiento', 'remito', 'despachante', 'status', 'fecha_envio', 'created_at']
    list_filter = ['status', 'fecha_envio', 'created_at']
    search_fields = ['numero_seguimiento', 'remito__numero_remito', 'despachante__razon_social']
    ordering = ['-created_at']


@admin.register(Comunicacion)
class ComunicacionAdmin(admin.ModelAdmin):
    """Admin interface for Comunicacion model."""
    
    list_display = ['usuario', 'entidad_tipo', 'entidad_id', 'created_at']
    list_filter = ['entidad_tipo', 'created_at']
    search_fields = ['usuario__email', 'contenido']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    """Admin interface for Actividad model."""
    
    list_display = ['usuario', 'tipo', 'tipo_entidad', 'id_entidad', 'fecha']
    list_filter = ['tipo', 'tipo_entidad', 'fecha']
    search_fields = ['usuario__email', 'id_entidad']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
    
    def has_add_permission(self, request):
        """Disable adding activities manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing activities."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disable deleting activities."""
        return False
