-- =====================================================
-- COMPRAS-SOFT DATABASE INITIALIZATION SCRIPT
-- PostgreSQL Database Schema for Procurement System
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- ENUM TYPES
-- =====================================================

-- User role enumeration
CREATE TYPE rol_usuario AS ENUM ('VENDEDOR', 'COMPRADOR', 'ADMINISTRADOR', 'SUPERVISOR');

-- Activity type enumeration
CREATE TYPE tipo_de_actividad AS ENUM ('CREATE', 'UPDATE', 'DELETE', 'VIEW', 'APPROVE', 'REJECT');

-- Entity type enumeration  
CREATE TYPE tipo_de_entidad AS ENUM (
    'PROVEEDOR', 'CLIENTE', 'ARTICULO', 'COTIZACION', 'ORDEN_COMPRA', 
    'PEDIDO_COTIZACION', 'SOLPED', 'REMITO', 'ENVIO', 'USUARIO'
);

-- Article usage level enumeration
CREATE TYPE nivel_uso_articulo AS ENUM ('DOMESTICO', 'COMERCIAL', 'INDUSTRIAL', 'CRITICO');

-- Status enumerations for different entities
CREATE TYPE status_proveedor AS ENUM ('ACTIVO', 'INACTIVO', 'SUSPENDIDO', 'PENDIENTE_APROBACION');
CREATE TYPE status_cliente AS ENUM ('ACTIVO', 'INACTIVO', 'SUSPENDIDO', 'PENDIENTE_APROBACION');
CREATE TYPE status_articulo AS ENUM ('ACTIVO', 'INACTIVO', 'DESCONTINUADO', 'PENDIENTE_APROBACION');
CREATE TYPE status_cotizacion AS ENUM ('BORRADOR', 'ENVIADA', 'RECIBIDA', 'EVALUADA', 'ACEPTADA', 'RECHAZADA', 'VENCIDA');
CREATE TYPE status_orden_compra AS ENUM ('BORRADOR', 'ENVIADA', 'CONFIRMADA', 'EN_PROCESO', 'COMPLETADA', 'CANCELADA');
CREATE TYPE status_pedido_cotizacion AS ENUM ('PENDIENTE DE RESPUESTA', 'BORRADOR', 'ENVIADO', 'RESPONDIDO', 'VENCIDO', 'CANCELADO');
CREATE TYPE status_solped AS ENUM ('BORRADOR', 'ENVIADA', 'APROBADA', 'RECHAZADA', 'EN_PROCESO', 'COMPLETADA');
CREATE TYPE status_remito AS ENUM ('BORRADOR', 'ENVIADO', 'EN_TRANSITO', 'ENTREGADO', 'DEVUELTO');
CREATE TYPE status_envio AS ENUM ('PREPARANDO', 'EN_TRANSITO', 'ENTREGADO', 'DEVUELTO', 'PERDIDO', 'DEMORADO');

-- Unit types for measurements
CREATE TYPE unidad_longitud AS ENUM ('MM', 'CM', 'DM', 'M');
CREATE TYPE unidad_peso AS ENUM ('G', 'KG', 'TON');
CREATE TYPE unidad_cantidad AS ENUM ('UNIDAD', 'CAJA', 'PALLET', 'KG', 'LITRO', 'METRO', 'M2', 'M3');
CREATE TYPE unidad_moneda AS ENUM ('ARS', 'USD', 'EUR', 'BRL');

-- =====================================================
-- CORE ENTITY TABLES
-- =====================================================

-- Users table
CREATE TABLE usuarios ( -- Esto va a ser un custom user de Django framework
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol rol_usuario NOT NULL DEFAULT 'VENDEDOR',
    status BOOLEAN NOT NULL DEFAULT true,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID
);

-- Suppliers table
CREATE TABLE proveedores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    razon_social VARCHAR(765) NOT NULL, -- 3 lines * 255 chars
    localizacion TEXT,
    cuit VARCHAR(13) UNIQUE, -- Format: XX-XXXXXXXX-X
    status status_proveedor NOT NULL DEFAULT 'PENDIENTE_APROBACION',
    es_proveedor_nacional BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Clients table
CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    razon_social VARCHAR(765) NULL,
    localizacion TEXT,
    cuit VARCHAR(13) UNIQUE,
    status status_cliente NOT NULL DEFAULT 'ACTIVO',
    web_page TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    contact_name VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Delivery methods table
CREATE TABLE formas_de_entrega (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Articles table
CREATE TABLE articulos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    descripcion TEXT NOT NULL,
    marca VARCHAR(255),
    modelo VARCHAR(255),
    tipo VARCHAR(255),
    palabras_claves TEXT[], -- Array of keywords
    familia VARCHAR(255),
    sub_familia VARCHAR(255),
    material_principal VARCHAR(255),
    material_secundario VARCHAR(255),
    codigo_fabricante VARCHAR(255),
    especificacion_tecnica JSONB,
    tags TEXT[], -- Array of tags
    industria VARCHAR(255), -- tienen que ser enums cada uno (SEGUIR EL DECISION TREE!)
    url_ficha_tecnica TEXT,
    url_manual_tecnico TEXT,
    url_imagen_principal TEXT,
    nivel_uso nivel_uso_articulo,
    status status_articulo NOT NULL DEFAULT 'PENDIENTE_APROBACION',
    
    -- Weight fields
    peso_valor DECIMAL(10,3),
    peso_unidad unidad_peso,
    
    -- Dimension fields (length, width, height)
    largo_valor DECIMAL(10,3),
    largo_unidad unidad_longitud,
    alto_valor DECIMAL(10,3),
    alto_unidad unidad_longitud,
    ancho_valor DECIMAL(10,3),
    ancho_unidad unidad_longitud,
    
    -- Category fields
    categoria_lvl1 VARCHAR(255), -- tienen que ser enums cada uno (SEGUIR EL DECISION TREE!!)
    categoria_lvl2 VARCHAR(255), -- tienen que ser enums cada uno (SEGUIR EL DECISION TREE!)
    categoria_lvl3 VARCHAR(255), -- tienen que ser enums cada uno (SEGUIR EL DECISION TREE!)
    categoria_lvl4 VARCHAR(255), -- tienen que ser enums cada uno (SEGUIR EL DECISION TREE!)
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Shipping companies table
CREATE TABLE despachantes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    razon_social VARCHAR(765) NOT NULL,
    cuit VARCHAR(13) UNIQUE,
    direccion TEXT,
    telefono VARCHAR(20),
    telefono_secundario VARCHAR(20),
    email VARCHAR(255),
    contact_name VARCHAR(255),
    email_secundario VARCHAR(255),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- =====================================================
-- BUSINESS PROCESS TABLES
-- =====================================================

-- Purchase requests (Solped)
CREATE TABLE solpeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nro_solped INTEGER NOT NULL UNIQUE,
    status status_solped NOT NULL DEFAULT 'BORRADOR',
    pedido_cotizacion_id UUID REFERENCES pedidos_de_cotizacion(id),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Solped details
CREATE TABLE detalle_solpeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    solped_id UUID NOT NULL REFERENCES solpeds(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Quote requests to suppliers
CREATE TABLE pedidos_de_cotizacion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id),
    status status_pedido_cotizacion NOT NULL DEFAULT 'BORRADOR',
    fecha_vencimiento DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Quote requests to specific suppliers
CREATE TABLE pedidos_cotizacion_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proveedor_id UUID NOT NULL REFERENCES proveedores(id),
    status status_pedido_cotizacion NOT NULL DEFAULT 'BORRADOR',
    fecha_vencimiento DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Quote request details to suppliers
CREATE TABLE detalle_pedido_cotizacion_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pedido_cotizacion_proveedor_id UUID NOT NULL REFERENCES pedidos_cotizacion_proveedor(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Supplier quotations
CREATE TABLE cotizaciones_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proveedor_id UUID NOT NULL REFERENCES proveedores(id),
    pedido_cotizacion_proveedor_id UUID REFERENCES pedidos_cotizacion_proveedor(id),
    status status_cotizacion NOT NULL DEFAULT 'BORRADOR',
    fecha_vencimiento DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Supplier quotation details
CREATE TABLE detalle_cotizacion_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cotizacion_proveedor_id UUID NOT NULL REFERENCES cotizaciones_proveedor(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Price fields
    precio_unitario_valor DECIMAL(15,2) NOT NULL,
    precio_unitario_moneda unidad_moneda NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Final quotations to clients
CREATE TABLE cotizaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id),
    margen DECIMAL(5,2), -- Percentage margin
    status status_cotizacion NOT NULL DEFAULT 'BORRADOR',
    fecha_vencimiento DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Purchase orders to suppliers
CREATE TABLE ordenes_compra_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proveedor_id UUID NOT NULL REFERENCES proveedores(id),
    numero_orden VARCHAR(50) UNIQUE,
    status status_orden_compra NOT NULL DEFAULT 'BORRADOR',
    fecha_entrega_estimada DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Purchase order details to suppliers
CREATE TABLE detalle_orden_compra_proveedor (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orden_compra_proveedor_id UUID NOT NULL REFERENCES ordenes_compra_proveedor(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Price fields
    precio_unitario_valor DECIMAL(15,2) NOT NULL,
    precio_unitario_moneda unidad_moneda NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Sales orders from clients
CREATE TABLE ordenes_compra_cliente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id),
    numero_orden VARCHAR(50) UNIQUE,
    status status_orden_compra NOT NULL DEFAULT 'BORRADOR',
    fecha_entrega_estimada DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Sales order details from clients
CREATE TABLE detalle_orden_compra_cliente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orden_compra_cliente_id UUID NOT NULL REFERENCES ordenes_compra_cliente(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Price fields
    precio_valor DECIMAL(15,2) NOT NULL,
    precio_moneda unidad_moneda NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Delivery receipts
CREATE TABLE remitos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    destinatario_id UUID NOT NULL REFERENCES clientes(id),
    numero_remito VARCHAR(50) UNIQUE,
    status status_remito NOT NULL DEFAULT 'BORRADOR',
    fecha_envio DATE,
    fecha_entrega_estimada DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Delivery receipt details
CREATE TABLE detalle_remito (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    remito_id UUID NOT NULL REFERENCES remitos(id),
    articulo_id UUID NOT NULL REFERENCES articulos(id),
    
    -- Quantity fields
    cantidad_valor DECIMAL(15,3) NOT NULL,
    cantidad_unidad unidad_cantidad NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Shipments
CREATE TABLE envios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    remito_id UUID NOT NULL REFERENCES remitos(id),
    despachante_id UUID NOT NULL REFERENCES despachantes(id),
    numero_seguimiento VARCHAR(255),
    status status_envio NOT NULL DEFAULT 'PREPARANDO',
    fecha_envio DATE,
    fecha_entrega_real DATE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Communications/Messages
CREATE TABLE comunicaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    contenido TEXT NOT NULL,
    entidad_tipo tipo_de_entidad,
    entidad_id UUID,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id)
);

-- Activity log
CREATE TABLE actividades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tipo tipo_de_actividad NOT NULL,
    id_entidad UUID NOT NULL,
    tipo_entidad tipo_de_entidad NOT NULL,
    data JSONB,
    
    -- Audit fields (no soft delete for audit log)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- JUNCTION TABLES (Many-to-Many Relationships)
-- =====================================================

-- Supplier delivery methods junction table
CREATE TABLE proveedor_formas_entrega (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proveedor_id UUID NOT NULL REFERENCES proveedores(id),
    forma_entrega_id UUID NOT NULL REFERENCES formas_de_entrega(id),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id),
    
    UNIQUE(proveedor_id, forma_entrega_id)
);

-- Quote request to solped relationship
CREATE TABLE pedido_cotizacion_solpeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pedido_cotizacion_id UUID NOT NULL REFERENCES pedidos_de_cotizacion(id),
    solped_id UUID NOT NULL REFERENCES solpeds(id),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id),
    
    UNIQUE(pedido_cotizacion_id, solped_id)
);

-- Final quotation to solped relationship
CREATE TABLE cotizacion_solpeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cotizacion_id UUID NOT NULL REFERENCES cotizaciones(id),
    solped_id UUID NOT NULL REFERENCES solpeds(id),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id),
    
    UNIQUE(cotizacion_id, solped_id)
);

-- Winning quotation details (ganadores)
CREATE TABLE cotizacion_ganadores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cotizacion_id UUID NOT NULL REFERENCES cotizaciones(id),
    detalle_cotizacion_proveedor_id UUID NOT NULL REFERENCES detalle_cotizacion_proveedor(id),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    updated_by UUID REFERENCES usuarios(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES usuarios(id),
    
    UNIQUE(cotizacion_id, detalle_cotizacion_proveedor_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User indexes
CREATE INDEX idx_usuarios_email ON usuarios(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_usuarios_rol ON usuarios(rol) WHERE deleted_at IS NULL;

-- Supplier indexes
CREATE INDEX idx_proveedores_cuit ON proveedores(cuit) WHERE deleted_at IS NULL;
CREATE INDEX idx_proveedores_status ON proveedores(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_proveedores_razon_social ON proveedores USING gin(to_tsvector('spanish', razon_social)) WHERE deleted_at IS NULL;

-- Client indexes
CREATE INDEX idx_clientes_cuit ON clientes(cuit) WHERE deleted_at IS NULL;
CREATE INDEX idx_clientes_status ON clientes(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_clientes_razon_social ON clientes USING gin(to_tsvector('spanish', razon_social)) WHERE deleted_at IS NULL;

-- Article indexes
CREATE INDEX idx_articulos_status ON articulos(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_familia ON articulos(familia) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_marca ON articulos(marca) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_descripcion ON articulos USING gin(to_tsvector('spanish', descripcion)) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_palabras_claves ON articulos USING gin(palabras_claves) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_tags ON articulos USING gin(tags) WHERE deleted_at IS NULL;
CREATE INDEX idx_articulos_categoria_lvl1 ON articulos(categoria_lvl1) WHERE deleted_at IS NULL;

-- Business process indexes
CREATE INDEX idx_solpeds_nro ON solpeds(nro_solped) WHERE deleted_at IS NULL;
CREATE INDEX idx_solpeds_status ON solpeds(status) WHERE deleted_at IS NULL;

CREATE INDEX idx_cotizaciones_proveedor_status ON cotizaciones_proveedor(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_cotizaciones_proveedor_fecha ON cotizaciones_proveedor(fecha_vencimiento) WHERE deleted_at IS NULL;

CREATE INDEX idx_cotizaciones_status ON cotizaciones(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_cotizaciones_cliente ON cotizaciones(cliente_id) WHERE deleted_at IS NULL;

CREATE INDEX idx_ordenes_compra_proveedor_status ON ordenes_compra_proveedor(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_ordenes_compra_proveedor_numero ON ordenes_compra_proveedor(numero_orden) WHERE deleted_at IS NULL;

CREATE INDEX idx_ordenes_compra_cliente_status ON ordenes_compra_cliente(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_ordenes_compra_cliente_numero ON ordenes_compra_cliente(numero_orden) WHERE deleted_at IS NULL;

-- Audit indexes
CREATE INDEX idx_actividades_usuario ON actividades(usuario_id);
CREATE INDEX idx_actividades_fecha ON actividades(fecha);
CREATE INDEX idx_actividades_entidad ON actividades(tipo_entidad, id_entidad);
CREATE INDEX idx_actividades_tipo ON actividades(tipo);

-- Foreign key indexes for better join performance
CREATE INDEX idx_detalle_solpeds_solped ON detalle_solpeds(solped_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_detalle_solpeds_articulo ON detalle_solpeds(articulo_id) WHERE deleted_at IS NULL;

CREATE INDEX idx_detalle_cotizacion_proveedor_cotizacion ON detalle_cotizacion_proveedor(cotizacion_proveedor_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_detalle_cotizacion_proveedor_articulo ON detalle_cotizacion_proveedor(articulo_id) WHERE deleted_at IS NULL;

CREATE INDEX idx_detalle_orden_compra_proveedor_orden ON detalle_orden_compra_proveedor(orden_compra_proveedor_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_detalle_orden_compra_cliente_orden ON detalle_orden_compra_cliente(orden_compra_cliente_id) WHERE deleted_at IS NULL;

CREATE INDEX idx_detalle_remito_remito ON detalle_remito(remito_id) WHERE deleted_at IS NULL;

-- =====================================================
-- AUDIT TRAIL FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to log activities
CREATE OR REPLACE FUNCTION log_activity()
RETURNS TRIGGER AS $$
DECLARE
    activity_type tipo_de_actividad;
    entity_type tipo_de_entidad;
    user_id UUID;
BEGIN
    -- Determine activity type
    IF TG_OP = 'INSERT' THEN
        activity_type = 'CREATE';
    ELSIF TG_OP = 'UPDATE' THEN
        activity_type = 'UPDATE';
    ELSIF TG_OP = 'DELETE' THEN
        activity_type = 'DELETE';
    END IF;
    
    -- Determine entity type based on table name
    CASE TG_TABLE_NAME
        WHEN 'usuarios' THEN entity_type = 'USUARIO';
        WHEN 'proveedores' THEN entity_type = 'PROVEEDOR';
        WHEN 'clientes' THEN entity_type = 'CLIENTE';
        WHEN 'articulos' THEN entity_type = 'ARTICULO';
        WHEN 'cotizaciones' THEN entity_type = 'COTIZACION';
        WHEN 'cotizaciones_proveedor' THEN entity_type = 'COTIZACION';
        WHEN 'ordenes_compra_proveedor' THEN entity_type = 'ORDEN_COMPRA';
        WHEN 'ordenes_compra_cliente' THEN entity_type = 'ORDEN_COMPRA';
        WHEN 'pedidos_cotizacion_proveedor' THEN entity_type = 'PEDIDO_COTIZACION';
        WHEN 'solpeds' THEN entity_type = 'SOLPED';
        WHEN 'remitos' THEN entity_type = 'REMITO';
        WHEN 'envios' THEN entity_type = 'ENVIO';
        ELSE entity_type = 'USUARIO'; -- Default fallback
    END CASE;
    
    -- Get user ID from the record
    IF TG_OP = 'DELETE' THEN
        user_id = OLD.updated_by;
        INSERT INTO actividades (usuario_id, tipo, id_entidad, tipo_entidad, data)
        VALUES (user_id, activity_type, OLD.id, entity_type, row_to_json(OLD));
    ELSE
        user_id = NEW.updated_by;
        INSERT INTO actividades (usuario_id, tipo, id_entidad, tipo_entidad, data)
        VALUES (user_id, activity_type, NEW.id, entity_type, row_to_json(NEW));
    END IF;
    
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at on all tables with audit fields
CREATE TRIGGER trigger_usuarios_updated_at BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_proveedores_updated_at BEFORE UPDATE ON proveedores FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_clientes_updated_at BEFORE UPDATE ON clientes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_formas_de_entrega_updated_at BEFORE UPDATE ON formas_de_entrega FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_articulos_updated_at BEFORE UPDATE ON articulos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_despachantes_updated_at BEFORE UPDATE ON despachantes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_solpeds_updated_at BEFORE UPDATE ON solpeds FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_solpeds_updated_at BEFORE UPDATE ON detalle_solpeds FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_pedidos_de_cotizacion_updated_at BEFORE UPDATE ON pedidos_de_cotizacion FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_pedidos_cotizacion_proveedor_updated_at BEFORE UPDATE ON pedidos_cotizacion_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_pedido_cotizacion_proveedor_updated_at BEFORE UPDATE ON detalle_pedido_cotizacion_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_cotizaciones_proveedor_updated_at BEFORE UPDATE ON cotizaciones_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_cotizacion_proveedor_updated_at BEFORE UPDATE ON detalle_cotizacion_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_cotizaciones_updated_at BEFORE UPDATE ON cotizaciones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_ordenes_compra_proveedor_updated_at BEFORE UPDATE ON ordenes_compra_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_orden_compra_proveedor_updated_at BEFORE UPDATE ON detalle_orden_compra_proveedor FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_ordenes_compra_cliente_updated_at BEFORE UPDATE ON ordenes_compra_cliente FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_orden_compra_cliente_updated_at BEFORE UPDATE ON detalle_orden_compra_cliente FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_remitos_updated_at BEFORE UPDATE ON remitos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_detalle_remito_updated_at BEFORE UPDATE ON detalle_remito FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_envios_updated_at BEFORE UPDATE ON envios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_comunicaciones_updated_at BEFORE UPDATE ON comunicaciones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create audit trail triggers for main entities
CREATE TRIGGER trigger_usuarios_audit AFTER INSERT OR UPDATE OR DELETE ON usuarios FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_proveedores_audit AFTER INSERT OR UPDATE OR DELETE ON proveedores FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_clientes_audit AFTER INSERT OR UPDATE OR DELETE ON clientes FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_articulos_audit AFTER INSERT OR UPDATE OR DELETE ON articulos FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_cotizaciones_audit AFTER INSERT OR UPDATE OR DELETE ON cotizaciones FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_cotizaciones_proveedor_audit AFTER INSERT OR UPDATE OR DELETE ON cotizaciones_proveedor FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_ordenes_compra_proveedor_audit AFTER INSERT OR UPDATE OR DELETE ON ordenes_compra_proveedor FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_ordenes_compra_cliente_audit AFTER INSERT OR UPDATE OR DELETE ON ordenes_compra_cliente FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_solpeds_audit AFTER INSERT OR UPDATE OR DELETE ON solpeds FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_remitos_audit AFTER INSERT OR UPDATE OR DELETE ON remitos FOR EACH ROW EXECUTE FUNCTION log_activity();
CREATE TRIGGER trigger_envios_audit AFTER INSERT OR UPDATE OR DELETE ON envios FOR EACH ROW EXECUTE FUNCTION log_activity();

-- =====================================================
-- BUSINESS RULES AND CONSTRAINTS
-- =====================================================

-- Check constraints for business rules
ALTER TABLE articulos ADD CONSTRAINT chk_peso_positivo CHECK (peso_valor IS NULL OR peso_valor > 0);
ALTER TABLE articulos ADD CONSTRAINT chk_dimensiones_positivas CHECK (
    (largo_valor IS NULL OR largo_valor > 0) AND
    (alto_valor IS NULL OR alto_valor > 0) AND
    (ancho_valor IS NULL OR ancho_valor > 0)
);

ALTER TABLE detalle_cotizacion_proveedor ADD CONSTRAINT chk_cantidad_positiva CHECK (cantidad_valor > 0);
ALTER TABLE detalle_cotizacion_proveedor ADD CONSTRAINT chk_precio_positivo CHECK (precio_unitario_valor > 0);

ALTER TABLE detalle_orden_compra_proveedor ADD CONSTRAINT chk_cantidad_positiva CHECK (cantidad_valor > 0);
ALTER TABLE detalle_orden_compra_proveedor ADD CONSTRAINT chk_precio_positivo CHECK (precio_unitario_valor > 0);

ALTER TABLE detalle_orden_compra_cliente ADD CONSTRAINT chk_cantidad_positiva CHECK (cantidad_valor > 0);
ALTER TABLE detalle_orden_compra_cliente ADD CONSTRAINT chk_precio_positivo CHECK (precio_valor > 0);

ALTER TABLE detalle_remito ADD CONSTRAINT chk_cantidad_positiva CHECK (cantidad_valor > 0);
ALTER TABLE detalle_solpeds ADD CONSTRAINT chk_cantidad_positiva CHECK (cantidad_valor > 0);

ALTER TABLE cotizaciones ADD CONSTRAINT chk_margen_valido CHECK (margen IS NULL OR (margen >= 0 AND margen <= 100));

-- CUIT format validation (basic)
ALTER TABLE proveedores ADD CONSTRAINT chk_cuit_formato CHECK (cuit IS NULL OR cuit ~ '^\d{2}-\d{8}-\d{1}$');
ALTER TABLE clientes ADD CONSTRAINT chk_cuit_formato CHECK (cuit IS NULL OR cuit ~ '^\d{2}-\d{8}-\d{1}$');
ALTER TABLE despachantes ADD CONSTRAINT chk_cuit_formato CHECK (cuit IS NULL OR cuit ~ '^\d{2}-\d{8}-\d{1}$');

-- Email format validation
ALTER TABLE usuarios ADD CONSTRAINT chk_email_formato CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- =====================================================
-- USEFUL VIEWS
-- =====================================================

-- View for active suppliers with delivery methods
CREATE VIEW v_proveedores_activos AS
SELECT 
    p.id,
    p.razon_social,
    p.cuit,
    p.localizacion,
    p.status,
    array_agg(fe.nombre) as formas_entrega
FROM proveedores p
LEFT JOIN proveedor_formas_entrega pfe ON p.id = pfe.proveedor_id AND pfe.deleted_at IS NULL
LEFT JOIN formas_de_entrega fe ON pfe.forma_entrega_id = fe.id AND fe.deleted_at IS NULL
WHERE p.deleted_at IS NULL AND p.status = 'ACTIVO'
GROUP BY p.id, p.razon_social, p.cuit, p.localizacion, p.status;

-- View for active articles with full details
CREATE VIEW v_articulos_activos AS
SELECT 
    id,
    descripcion,
    marca,
    modelo,
    familia,
    sub_familia,
    categoria_lvl1,
    categoria_lvl2,
    categoria_lvl3,
    categoria_lvl4,
    nivel_uso,
    peso_valor || ' ' || peso_unidad as peso,
    largo_valor || ' ' || largo_unidad as largo,
    alto_valor || ' ' || alto_unidad as alto,
    ancho_valor || ' ' || ancho_unidad as ancho,
    status,
    created_at
FROM articulos
WHERE deleted_at IS NULL AND status = 'ACTIVO';

-- View for quotation summary
CREATE VIEW v_resumen_cotizaciones AS
SELECT 
    c.id,
    cl.razon_social as cliente,
    c.status,
    c.margen,
    c.fecha_vencimiento,
    COUNT(cg.id) as items_ganadores,
    c.created_at
FROM cotizaciones c
JOIN clientes cl ON c.cliente_id = cl.id
LEFT JOIN cotizacion_ganadores cg ON c.id = cg.cotizacion_id AND cg.deleted_at IS NULL
WHERE c.deleted_at IS NULL
GROUP BY c.id, cl.razon_social, c.status, c.margen, c.fecha_vencimiento, c.created_at;

-- =====================================================
-- INITIAL DATA SETUP
-- =====================================================

-- Insert default admin user (password should be hashed in real implementation)
INSERT INTO usuarios (email, password, rol, created_by, updated_by) 
VALUES ('admin@compras-soft.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXig/8VfuFvO', 'ADMINISTRADOR', 
        (SELECT id FROM usuarios WHERE email = 'admin@compras-soft.com' LIMIT 1),
        (SELECT id FROM usuarios WHERE email = 'admin@compras-soft.com' LIMIT 1))
ON CONFLICT (email) DO NOTHING;

-- Insert default delivery methods
INSERT INTO formas_de_entrega (nombre, descripcion) VALUES 
('Retiro en sucursal', 'El cliente retira el producto en nuestras instalaciones'),
('Envío a domicilio', 'Entrega en el domicilio del cliente'),
('Envío express', 'Entrega express en 24-48 horas'),
('Flete terrestre', 'Transporte por camión para productos grandes'),
('Courier', 'Servicio de mensajería para productos pequeños');

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON DATABASE postgres IS 'Sistema de gestión de compras y cotizaciones';

COMMENT ON TABLE usuarios IS 'Usuarios del sistema con roles y permisos';
COMMENT ON TABLE proveedores IS 'Proveedores de productos y servicios';
COMMENT ON TABLE clientes IS 'Clientes que solicitan cotizaciones';
COMMENT ON TABLE articulos IS 'Catálogo de productos disponibles';
COMMENT ON TABLE formas_de_entrega IS 'Métodos de entrega disponibles';
COMMENT ON TABLE solpeds IS 'Solicitudes de pedido internas';
COMMENT ON TABLE cotizaciones_proveedor IS 'Cotizaciones recibidas de proveedores';
COMMENT ON TABLE cotizaciones IS 'Cotizaciones finales enviadas a clientes';
COMMENT ON TABLE ordenes_compra_proveedor IS 'Órdenes de compra enviadas a proveedores';
COMMENT ON TABLE ordenes_compra_cliente IS 'Órdenes de compra recibidas de clientes';
COMMENT ON TABLE remitos IS 'Remitos de entrega';
COMMENT ON TABLE envios IS 'Seguimiento de envíos';
COMMENT ON TABLE actividades IS 'Log de auditoría del sistema';

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Total tables created: %', (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE');
    RAISE NOTICE 'Total indexes created: %', (SELECT count(*) FROM pg_indexes WHERE schemaname = 'public');
    RAISE NOTICE 'Total triggers created: %', (SELECT count(*) FROM information_schema.triggers WHERE trigger_schema = 'public');
END $$;
