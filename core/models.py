"""
Core entity models for the procurement system.
"""

import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from djmoney.models.fields import MoneyField


# ==============================================================================
# ENUMERATIONS
# ==============================================================================

class StatusProveedor(models.TextChoices):
    """Supplier status enumeration."""
    ACTIVO = 'ACTIVO', 'Activo'
    INACTIVO = 'INACTIVO', 'Inactivo'
    SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'
    PENDIENTE_APROBACION = 'PENDIENTE_APROBACION', 'Pendiente de Aprobación'


class StatusCliente(models.TextChoices):
    """Client status enumeration."""
    ACTIVO = 'ACTIVO', 'Activo'
    INACTIVO = 'INACTIVO', 'Inactivo'
    SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'
    PENDIENTE_APROBACION = 'PENDIENTE_APROBACION', 'Pendiente de Aprobación'


class StatusArticulo(models.TextChoices):
    """Article status enumeration."""
    ACTIVO = 'ACTIVO', 'Activo'
    INACTIVO = 'INACTIVO', 'Inactivo'
    DESCONTINUADO = 'DESCONTINUADO', 'Descontinuado'
    PENDIENTE_APROBACION = 'PENDIENTE_APROBACION', 'Pendiente de Aprobación'


class NivelUsoArticulo(models.TextChoices):
    """Article usage level enumeration."""
    DOMESTICO = 'DOMESTICO', 'Doméstico'
    COMERCIAL = 'COMERCIAL', 'Comercial'
    INDUSTRIAL = 'INDUSTRIAL', 'Industrial'
    CRITICO = 'CRITICO', 'Crítico'


class UnidadLongitud(models.TextChoices):
    """Length unit enumeration."""
    MM = 'MM', 'Milímetros'
    CM = 'CM', 'Centímetros'
    DM = 'DM', 'Decímetros'
    M = 'M', 'Metros'


class UnidadPeso(models.TextChoices):
    """Weight unit enumeration."""
    G = 'G', 'Gramos'
    KG = 'KG', 'Kilogramos'
    TON = 'TON', 'Toneladas'


class UnidadCantidad(models.TextChoices):
    """Quantity unit enumeration."""
    UNIDAD = 'UNIDAD', 'Unidad'
    CAJA = 'CAJA', 'Caja'
    PALLET = 'PALLET', 'Pallet'
    KG = 'KG', 'Kilogramo'
    LITRO = 'LITRO', 'Litro'
    METRO = 'METRO', 'Metro'
    M2 = 'M2', 'Metro Cuadrado'
    M3 = 'M3', 'Metro Cúbico'


# ==============================================================================
# ABSTRACT BASE MODEL
# ==============================================================================

class BaseModel(SafeDeleteModel):
    """Abstract base model with common fields."""
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Audit fields
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_creados',
        verbose_name='Creado por'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_actualizados',
        verbose_name='Actualizado por'
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_eliminados',
        verbose_name='Eliminado por'
    )
    
    class Meta:
        abstract = True


# ==============================================================================
# CORE MODELS
# ==============================================================================

class Proveedor(BaseModel):
    """Supplier model."""
    
    razon_social = models.CharField('Razón Social', max_length=765)
    localizacion = models.TextField('Localización', blank=True)
    cuit = models.CharField('CUIT', max_length=13, unique=True, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=25,
        choices=StatusProveedor.choices,
        default=StatusProveedor.PENDIENTE_APROBACION
    )
    es_proveedor_nacional = models.BooleanField('Proveedor Nacional', default=False)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cuit'], name='idx_proveedores_cuit'),
            models.Index(fields=['status'], name='idx_proveedores_status'),
        ]
    
    def __str__(self):
        return self.razon_social


class Cliente(BaseModel):
    """Client model."""
    
    razon_social = models.CharField('Razón Social', max_length=765, null=True, blank=True)
    localizacion = models.TextField('Localización', blank=True)
    cuit = models.CharField('CUIT', max_length=13, unique=True, null=True, blank=True)
    status = models.CharField(
        'Estado',
        max_length=25,
        choices=StatusCliente.choices,
        default=StatusCliente.ACTIVO
    )
    web_page = models.URLField('Página Web', blank=True)
    phone_number = models.CharField('Teléfono', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    contact_name = models.CharField('Nombre de Contacto', max_length=255, blank=True)
    contact_phone = models.CharField('Teléfono de Contacto', max_length=20, blank=True)
    contact_email = models.EmailField('Email de Contacto', blank=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cuit'], name='idx_clientes_cuit'),
            models.Index(fields=['status'], name='idx_clientes_status'),
        ]
    
    def __str__(self):
        return self.razon_social or self.email or str(self.id)


class FormaDeEntrega(BaseModel):
    """Delivery method model."""
    
    nombre = models.CharField('Nombre', max_length=255)
    descripcion = models.TextField('Descripción', blank=True)
    
    class Meta:
        verbose_name = 'Forma de Entrega'
        verbose_name_plural = 'Formas de Entrega'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Articulo(BaseModel):
    """Article/Product model."""
    
    descripcion = models.TextField('Descripción')
    marca = models.CharField('Marca', max_length=255, blank=True)
    modelo = models.CharField('Modelo', max_length=255, blank=True)
    tipo = models.CharField('Tipo', max_length=255, blank=True)
    palabras_claves = ArrayField(
        models.CharField(max_length=100),
        verbose_name='Palabras Clave',
        blank=True,
        default=list
    )
    familia = models.CharField('Familia', max_length=255, blank=True)
    sub_familia = models.CharField('Sub Familia', max_length=255, blank=True)
    material_principal = models.CharField('Material Principal', max_length=255, blank=True)
    material_secundario = models.CharField('Material Secundario', max_length=255, blank=True)
    codigo_fabricante = models.CharField('Código Fabricante', max_length=255, blank=True)
    especificacion_tecnica = models.JSONField('Especificación Técnica', null=True, blank=True)
    tags = ArrayField(
        models.CharField(max_length=100),
        verbose_name='Tags',
        blank=True,
        default=list
    )
    industria = models.CharField('Industria', max_length=255, blank=True)
    url_ficha_tecnica = models.URLField('URL Ficha Técnica', blank=True)
    url_manual_tecnico = models.URLField('URL Manual Técnico', blank=True)
    url_imagen_principal = models.URLField('URL Imagen Principal', blank=True)
    nivel_uso = models.CharField(
        'Nivel de Uso',
        max_length=20,
        choices=NivelUsoArticulo.choices,
        null=True,
        blank=True
    )
    status = models.CharField(
        'Estado',
        max_length=25,
        choices=StatusArticulo.choices,
        default=StatusArticulo.PENDIENTE_APROBACION
    )
    
    # Weight fields
    peso_valor = models.DecimalField('Peso', max_digits=10, decimal_places=3, null=True, blank=True)
    peso_unidad = models.CharField('Unidad de Peso', max_length=10, choices=UnidadPeso.choices, null=True, blank=True)
    
    # Dimension fields
    largo_valor = models.DecimalField('Largo', max_digits=10, decimal_places=3, null=True, blank=True)
    largo_unidad = models.CharField('Unidad de Largo', max_length=10, choices=UnidadLongitud.choices, null=True, blank=True)
    alto_valor = models.DecimalField('Alto', max_digits=10, decimal_places=3, null=True, blank=True)
    alto_unidad = models.CharField('Unidad de Alto', max_length=10, choices=UnidadLongitud.choices, null=True, blank=True)
    ancho_valor = models.DecimalField('Ancho', max_digits=10, decimal_places=3, null=True, blank=True)
    ancho_unidad = models.CharField('Unidad de Ancho', max_length=10, choices=UnidadLongitud.choices, null=True, blank=True)
    
    # Category fields
    categoria_lvl1 = models.CharField('Categoría Nivel 1', max_length=255, blank=True)
    categoria_lvl2 = models.CharField('Categoría Nivel 2', max_length=255, blank=True)
    categoria_lvl3 = models.CharField('Categoría Nivel 3', max_length=255, blank=True)
    categoria_lvl4 = models.CharField('Categoría Nivel 4', max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='idx_articulos_status'),
            models.Index(fields=['familia'], name='idx_articulos_familia'),
            models.Index(fields=['marca'], name='idx_articulos_marca'),
            models.Index(fields=['categoria_lvl1'], name='idx_articulos_categoria_lvl1'),
        ]
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.descripcion[:50]}" if self.marca else self.descripcion[:50]


class Despachante(BaseModel):
    """Shipping company model."""
    
    razon_social = models.CharField('Razón Social', max_length=765)
    cuit = models.CharField('CUIT', max_length=13, unique=True, null=True, blank=True)
    direccion = models.TextField('Dirección', blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    telefono_secundario = models.CharField('Teléfono Secundario', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    contact_name = models.CharField('Nombre de Contacto', max_length=255, blank=True)
    email_secundario = models.EmailField('Email Secundario', blank=True)
    
    class Meta:
        verbose_name = 'Despachante'
        verbose_name_plural = 'Despachantes'
        ordering = ['razon_social']
    
    def __str__(self):
        return self.razon_social


# ==============================================================================
# JUNCTION TABLES
# ==============================================================================

class ProveedorFormaEntrega(BaseModel):
    """Junction table for supplier delivery methods."""
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='formas_entrega',
        verbose_name='Proveedor'
    )
    forma_entrega = models.ForeignKey(
        FormaDeEntrega,
        on_delete=models.CASCADE,
        related_name='proveedores',
        verbose_name='Forma de Entrega'
    )
    
    class Meta:
        verbose_name = 'Proveedor-Forma de Entrega'
        verbose_name_plural = 'Proveedores-Formas de Entrega'
        unique_together = ['proveedor', 'forma_entrega']
    
    def __str__(self):
        return f"{self.proveedor} - {self.forma_entrega}"
