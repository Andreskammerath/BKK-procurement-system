"""
Procurement process models for the system.
"""

import uuid
from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from core.models import (
    BaseModel, Proveedor, Cliente, Articulo, Despachante,
    UnidadCantidad
)


# ==============================================================================
# ENUMERATIONS
# ==============================================================================

class StatusCotizacion(models.TextChoices):
    """Quotation status enumeration."""
    BORRADOR = 'BORRADOR', 'Borrador'
    ENVIADA = 'ENVIADA', 'Enviada'
    RECIBIDA = 'RECIBIDA', 'Recibida'
    EVALUADA = 'EVALUADA', 'Evaluada'
    ACEPTADA = 'ACEPTADA', 'Aceptada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'
    VENCIDA = 'VENCIDA', 'Vencida'


class StatusOrdenCompra(models.TextChoices):
    """Purchase order status enumeration."""
    BORRADOR = 'BORRADOR', 'Borrador'
    ENVIADA = 'ENVIADA', 'Enviada'
    CONFIRMADA = 'CONFIRMADA', 'Confirmada'
    EN_PROCESO = 'EN_PROCESO', 'En Proceso'
    COMPLETADA = 'COMPLETADA', 'Completada'
    CANCELADA = 'CANCELADA', 'Cancelada'


class StatusPedidoCotizacion(models.TextChoices):
    """Quote request status enumeration."""
    PENDIENTE_DE_RESPUESTA = 'PENDIENTE DE RESPUESTA', 'Pendiente de Respuesta'
    BORRADOR = 'BORRADOR', 'Borrador'
    ENVIADO = 'ENVIADO', 'Enviado'
    RESPONDIDO = 'RESPONDIDO', 'Respondido'
    VENCIDO = 'VENCIDO', 'Vencido'
    CANCELADO = 'CANCELADO', 'Cancelado'


class StatusSolped(models.TextChoices):
    """Purchase request status enumeration."""
    BORRADOR = 'BORRADOR', 'Borrador'
    ENVIADA = 'ENVIADA', 'Enviada'
    APROBADA = 'APROBADA', 'Aprobada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'
    EN_PROCESO = 'EN_PROCESO', 'En Proceso'
    COMPLETADA = 'COMPLETADA', 'Completada'


class StatusRemito(models.TextChoices):
    """Delivery receipt status enumeration."""
    BORRADOR = 'BORRADOR', 'Borrador'
    ENVIADO = 'ENVIADO', 'Enviado'
    EN_TRANSITO = 'EN_TRANSITO', 'En Tránsito'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    DEVUELTO = 'DEVUELTO', 'Devuelto'


class StatusEnvio(models.TextChoices):
    """Shipment status enumeration."""
    PREPARANDO = 'PREPARANDO', 'Preparando'
    EN_TRANSITO = 'EN_TRANSITO', 'En Tránsito'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    DEVUELTO = 'DEVUELTO', 'Devuelto'
    PERDIDO = 'PERDIDO', 'Perdido'
    DEMORADO = 'DEMORADO', 'Demorado'


class TipoDeActividad(models.TextChoices):
    """Activity type enumeration."""
    CREATE = 'CREATE', 'Crear'
    UPDATE = 'UPDATE', 'Actualizar'
    DELETE = 'DELETE', 'Eliminar'
    VIEW = 'VIEW', 'Ver'
    APPROVE = 'APPROVE', 'Aprobar'
    REJECT = 'REJECT', 'Rechazar'


class TipoDeEntidad(models.TextChoices):
    """Entity type enumeration."""
    PROVEEDOR = 'PROVEEDOR', 'Proveedor'
    CLIENTE = 'CLIENTE', 'Cliente'
    ARTICULO = 'ARTICULO', 'Artículo'
    COTIZACION = 'COTIZACION', 'Cotización'
    ORDEN_COMPRA = 'ORDEN_COMPRA', 'Orden de Compra'
    PEDIDO_COTIZACION = 'PEDIDO_COTIZACION', 'Pedido de Cotización'
    SOLPED = 'SOLPED', 'Solped'
    REMITO = 'REMITO', 'Remito'
    ENVIO = 'ENVIO', 'Envío'
    USUARIO = 'USUARIO', 'Usuario'


# ==============================================================================
# SOLPED MODELS (Purchase Requests)
# ==============================================================================

class Solped(BaseModel):
    """Purchase request model."""
    
    nro_solped = models.IntegerField('Número de Solped', unique=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusSolped.choices,
        default=StatusSolped.BORRADOR
    )
    
    class Meta:
        verbose_name = 'Solped'
        verbose_name_plural = 'Solpeds'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nro_solped'], name='idx_solpeds_nro'),
            models.Index(fields=['status'], name='idx_solpeds_status'),
        ]
    
    def __str__(self):
        return f"Solped #{self.nro_solped}"


class DetalleSolped(BaseModel):
    """Solped detail/line item model."""
    
    solped = models.ForeignKey(
        Solped,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Solped'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_solped',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    
    class Meta:
        verbose_name = 'Detalle de Solped'
        verbose_name_plural = 'Detalles de Solped'
        indexes = [
            models.Index(fields=['solped'], name='idx_detalle_solpeds_solped'),
            models.Index(fields=['articulo'], name='idx_detalle_solpeds_articulo'),
        ]
    
    def __str__(self):
        return f"{self.solped} - {self.articulo}"


# ==============================================================================
# QUOTE REQUEST MODELS
# ==============================================================================

class PedidoDeCotizacion(BaseModel):
    """Quote request to suppliers (from client)."""
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pedidos_cotizacion',
        verbose_name='Cliente'
    )
    status = models.CharField(
        'Estado',
        max_length=25,
        choices=StatusPedidoCotizacion.choices,
        default=StatusPedidoCotizacion.BORRADOR
    )
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Pedido de Cotización'
        verbose_name_plural = 'Pedidos de Cotización'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"PC-{self.id} - {self.cliente}"


class PedidoCotizacionProveedor(BaseModel):
    """Quote request to a specific supplier."""
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='pedidos_cotizacion',
        verbose_name='Proveedor'
    )
    status = models.CharField(
        'Estado',
        max_length=25,
        choices=StatusPedidoCotizacion.choices,
        default=StatusPedidoCotizacion.BORRADOR
    )
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Pedido de Cotización a Proveedor'
        verbose_name_plural = 'Pedidos de Cotización a Proveedores'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"PCP-{self.id} - {self.proveedor}"


class DetallePedidoCotizacionProveedor(BaseModel):
    """Quote request detail to supplier."""
    
    pedido_cotizacion_proveedor = models.ForeignKey(
        PedidoCotizacionProveedor,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Pedido Cotización Proveedor'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_pedido_cotizacion_proveedor',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    
    class Meta:
        verbose_name = 'Detalle de Pedido de Cotización a Proveedor'
        verbose_name_plural = 'Detalles de Pedidos de Cotización a Proveedores'
    
    def __str__(self):
        return f"{self.pedido_cotizacion_proveedor} - {self.articulo}"


# ==============================================================================
# QUOTATION MODELS
# ==============================================================================

class CotizacionProveedor(BaseModel):
    """Supplier quotation model."""
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='cotizaciones',
        verbose_name='Proveedor'
    )
    pedido_cotizacion_proveedor = models.ForeignKey(
        PedidoCotizacionProveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cotizaciones',
        verbose_name='Pedido de Cotización'
    )
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusCotizacion.choices,
        default=StatusCotizacion.BORRADOR
    )
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cotización de Proveedor'
        verbose_name_plural = 'Cotizaciones de Proveedores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='idx_cotiz_prov_status'),
            models.Index(fields=['fecha_vencimiento'], name='idx_cotiz_prov_fecha'),
        ]
    
    def __str__(self):
        return f"Cotización {self.id} - {self.proveedor}"


class DetalleCotizacionProveedor(BaseModel):
    """Supplier quotation detail model."""
    
    cotizacion_proveedor = models.ForeignKey(
        CotizacionProveedor,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Cotización Proveedor'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_cotizacion_proveedor',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    precio_unitario_valor = models.DecimalField('Precio Unitario', max_digits=15, decimal_places=2)
    precio_unitario_moneda = models.CharField('Moneda', max_length=3, default='ARS')
    
    class Meta:
        verbose_name = 'Detalle de Cotización de Proveedor'
        verbose_name_plural = 'Detalles de Cotizaciones de Proveedores'
        indexes = [
            models.Index(fields=['cotizacion_proveedor'], name='idx_det_cotiz_prov_cotiz'),
            models.Index(fields=['articulo'], name='idx_det_cotiz_prov_art'),
        ]
    
    def __str__(self):
        return f"{self.cotizacion_proveedor} - {self.articulo}"


class Cotizacion(BaseModel):
    """Final quotation to client model."""
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='cotizaciones',
        verbose_name='Cliente'
    )
    margen = models.DecimalField('Margen (%)', max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusCotizacion.choices,
        default=StatusCotizacion.BORRADOR
    )
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='idx_cotizaciones_status'),
            models.Index(fields=['cliente'], name='idx_cotizaciones_cliente'),
        ]
    
    def __str__(self):
        return f"Cotización {self.id} - {self.cliente}"


# ==============================================================================
# PURCHASE ORDER MODELS
# ==============================================================================

class OrdenCompraProveedor(BaseModel):
    """Purchase order to supplier model."""
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='ordenes_compra',
        verbose_name='Proveedor'
    )
    numero_orden = models.CharField('Número de Orden', max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusOrdenCompra.choices,
        default=StatusOrdenCompra.BORRADOR
    )
    fecha_entrega_estimada = models.DateField('Fecha de Entrega Estimada', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Orden de Compra a Proveedor'
        verbose_name_plural = 'Órdenes de Compra a Proveedores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='idx_ord_compra_prov_status'),
            models.Index(fields=['numero_orden'], name='idx_ord_compra_prov_num'),
        ]
    
    def __str__(self):
        return f"OC-{self.numero_orden or self.id} - {self.proveedor}"


class DetalleOrdenCompraProveedor(BaseModel):
    """Purchase order to supplier detail model."""
    
    orden_compra_proveedor = models.ForeignKey(
        OrdenCompraProveedor,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Orden de Compra Proveedor'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_orden_compra_proveedor',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    precio_unitario_valor = models.DecimalField('Precio Unitario', max_digits=15, decimal_places=2)
    precio_unitario_moneda = models.CharField('Moneda', max_length=3, default='ARS')
    
    class Meta:
        verbose_name = 'Detalle de Orden de Compra a Proveedor'
        verbose_name_plural = 'Detalles de Órdenes de Compra a Proveedores'
        indexes = [
            models.Index(fields=['orden_compra_proveedor'], name='idx_det_ord_prov_orden'),
        ]
    
    def __str__(self):
        return f"{self.orden_compra_proveedor} - {self.articulo}"


class OrdenCompraCliente(BaseModel):
    """Sales order from client model."""
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ordenes_compra',
        verbose_name='Cliente'
    )
    numero_orden = models.CharField('Número de Orden', max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusOrdenCompra.choices,
        default=StatusOrdenCompra.BORRADOR
    )
    fecha_entrega_estimada = models.DateField('Fecha de Entrega Estimada', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Orden de Compra de Cliente'
        verbose_name_plural = 'Órdenes de Compra de Clientes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='idx_ord_compra_cli_status'),
            models.Index(fields=['numero_orden'], name='idx_ord_compra_cli_num'),
        ]
    
    def __str__(self):
        return f"OCC-{self.numero_orden or self.id} - {self.cliente}"


class DetalleOrdenCompraCliente(BaseModel):
    """Sales order from client detail model."""
    
    orden_compra_cliente = models.ForeignKey(
        OrdenCompraCliente,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Orden de Compra Cliente'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_orden_compra_cliente',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    precio_valor = models.DecimalField('Precio', max_digits=15, decimal_places=2)
    precio_moneda = models.CharField('Moneda', max_length=3, default='ARS')
    
    class Meta:
        verbose_name = 'Detalle de Orden de Compra de Cliente'
        verbose_name_plural = 'Detalles de Órdenes de Compra de Clientes'
        indexes = [
            models.Index(fields=['orden_compra_cliente'], name='idx_det_ord_cli_orden'),
        ]
    
    def __str__(self):
        return f"{self.orden_compra_cliente} - {self.articulo}"


# ==============================================================================
# DELIVERY MODELS
# ==============================================================================

class Remito(BaseModel):
    """Delivery receipt model."""
    
    destinatario = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='remitos',
        verbose_name='Destinatario'
    )
    numero_remito = models.CharField('Número de Remito', max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusRemito.choices,
        default=StatusRemito.BORRADOR
    )
    fecha_envio = models.DateField('Fecha de Envío', null=True, blank=True)
    fecha_entrega_estimada = models.DateField('Fecha de Entrega Estimada', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Remito'
        verbose_name_plural = 'Remitos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Remito {self.numero_remito or self.id}"


class DetalleRemito(BaseModel):
    """Delivery receipt detail model."""
    
    remito = models.ForeignKey(
        Remito,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Remito'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='detalles_remito',
        verbose_name='Artículo'
    )
    cantidad_valor = models.DecimalField('Cantidad', max_digits=15, decimal_places=3)
    cantidad_unidad = models.CharField('Unidad', max_length=10, choices=UnidadCantidad.choices)
    
    class Meta:
        verbose_name = 'Detalle de Remito'
        verbose_name_plural = 'Detalles de Remitos'
        indexes = [
            models.Index(fields=['remito'], name='idx_detalle_remito_remito'),
        ]
    
    def __str__(self):
        return f"{self.remito} - {self.articulo}"


class Envio(BaseModel):
    """Shipment model."""
    
    remito = models.ForeignKey(
        Remito,
        on_delete=models.CASCADE,
        related_name='envios',
        verbose_name='Remito'
    )
    despachante = models.ForeignKey(
        Despachante,
        on_delete=models.CASCADE,
        related_name='envios',
        verbose_name='Despachante'
    )
    numero_seguimiento = models.CharField('Número de Seguimiento', max_length=255, blank=True)
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=StatusEnvio.choices,
        default=StatusEnvio.PREPARANDO
    )
    fecha_envio = models.DateField('Fecha de Envío', null=True, blank=True)
    fecha_entrega_real = models.DateField('Fecha de Entrega Real', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Envío {self.numero_seguimiento or self.id}"


# ==============================================================================
# COMMUNICATION & ACTIVITY MODELS
# ==============================================================================

class Comunicacion(BaseModel):
    """Communication/message model."""
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comunicaciones',
        verbose_name='Usuario'
    )
    contenido = models.TextField('Contenido')
    entidad_tipo = models.CharField(
        'Tipo de Entidad',
        max_length=20,
        choices=TipoDeEntidad.choices,
        null=True,
        blank=True
    )
    entidad_id = models.UUIDField('ID de Entidad', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Comunicación'
        verbose_name_plural = 'Comunicaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comunicación de {self.usuario} - {self.created_at}"


class Actividad(models.Model):
    """Activity log model (no soft delete for audit)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades',
        verbose_name='Usuario'
    )
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TipoDeActividad.choices)
    id_entidad = models.UUIDField('ID de Entidad')
    tipo_entidad = models.CharField('Tipo de Entidad', max_length=20, choices=TipoDeEntidad.choices)
    data = models.JSONField('Datos', null=True, blank=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['usuario'], name='idx_actividades_usuario'),
            models.Index(fields=['fecha'], name='idx_actividades_fecha'),
            models.Index(fields=['tipo_entidad', 'id_entidad'], name='idx_actividades_entidad'),
            models.Index(fields=['tipo'], name='idx_actividades_tipo'),
        ]
    
    def __str__(self):
        return f"{self.tipo} - {self.tipo_entidad} - {self.usuario}"


# ==============================================================================
# JUNCTION/RELATIONSHIP MODELS
# ==============================================================================

class PedidoCotizacionSolped(BaseModel):
    """Junction table for quote request and solped."""
    
    pedido_cotizacion = models.ForeignKey(
        PedidoDeCotizacion,
        on_delete=models.CASCADE,
        related_name='pedido_cotizacion_solpeds',
        verbose_name='Pedido de Cotización'
    )
    solped = models.ForeignKey(
        Solped,
        on_delete=models.CASCADE,
        related_name='pedido_cotizacion_solpeds',
        verbose_name='Solped'
    )
    
    class Meta:
        verbose_name = 'Pedido Cotización-Solped'
        verbose_name_plural = 'Pedidos Cotización-Solpeds'
        unique_together = ['pedido_cotizacion', 'solped']
    
    def __str__(self):
        return f"{self.pedido_cotizacion} - {self.solped}"


class CotizacionSolped(BaseModel):
    """Junction table for final quotation and solped."""
    
    cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.CASCADE,
        related_name='cotizacion_solpeds',
        verbose_name='Cotización'
    )
    solped = models.ForeignKey(
        Solped,
        on_delete=models.CASCADE,
        related_name='cotizacion_solpeds',
        verbose_name='Solped'
    )
    
    class Meta:
        verbose_name = 'Cotización-Solped'
        verbose_name_plural = 'Cotizaciones-Solpeds'
        unique_together = ['cotizacion', 'solped']
    
    def __str__(self):
        return f"{self.cotizacion} - {self.solped}"


class CotizacionGanador(BaseModel):
    """Winning quotation details (ganadores)."""
    
    cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.CASCADE,
        related_name='ganadores',
        verbose_name='Cotización'
    )
    detalle_cotizacion_proveedor = models.ForeignKey(
        DetalleCotizacionProveedor,
        on_delete=models.CASCADE,
        related_name='cotizaciones_ganadas',
        verbose_name='Detalle Cotización Proveedor'
    )
    
    class Meta:
        verbose_name = 'Cotización Ganadora'
        verbose_name_plural = 'Cotizaciones Ganadoras'
        unique_together = ['cotizacion', 'detalle_cotizacion_proveedor']
    
    def __str__(self):
        return f"Ganador: {self.cotizacion} - {self.detalle_cotizacion_proveedor}"
