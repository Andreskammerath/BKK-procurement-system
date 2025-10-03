# BKK Procurement System

Sistema integral de gestión de compras y cotizaciones desarrollado con Django 5.2.

## Características

- 🔐 **Autenticación personalizada** con roles de usuario (Vendedor, Comprador, Administrador, Supervisor)
- 📦 **Gestión completa de proveedores y clientes**
- 🛒 **Proceso de cotización y órdenes de compra**
- 📊 **Panel de administración mejorado** con Django Baton
- 🔍 **Búsqueda y filtrado avanzado**
- 📝 **Registro de actividades y auditoría**
- 🚀 **Tareas asíncronas** con Celery y Redis
- 💰 **Soporte multi-moneda** (ARS, USD, EUR, BRL)
- 🗑️ **Soft delete** en todos los modelos
- 🔒 **Permisos granulares** con Django Guardian

## Requisitos

- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (opcional pero recomendado)

## Instalación

### Opción 1: Con Docker (Recomendado)

1. **Clonar el repositorio** (si aplica)

2. **Copiar el archivo de variables de entorno:**
```bash
cp .env.example .env
```

3. **Construir y levantar los contenedores:**
```bash
docker-compose up --build
```

4. **En otra terminal, ejecutar las migraciones:**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

5. **Crear un superusuario:**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Acceder a la aplicación:**
- Aplicación: http://localhost:8000
- Admin: http://localhost:8000/admin/
- Flower (Celery monitor): http://localhost:5555

### Opción 2: Instalación Local

1. **Crear y activar entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. **Ejecutar migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo:**
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
BKK-procurement-system/
├── procurement_system/      # Configuración principal del proyecto
│   ├── settings.py          # Configuración Django
│   ├── urls.py              # URLs principales
│   ├── celery.py            # Configuración Celery
│   └── jinja2.py            # Configuración Jinja2
├── users/                   # App de usuarios
│   ├── models.py            # Modelo Usuario personalizado
│   ├── admin.py             # Admin de usuarios
│   └── views.py             # Vistas de autenticación
├── core/                    # App de entidades core
│   ├── models.py            # Proveedores, Clientes, Artículos
│   └── admin.py             # Admin de entidades core
├── procurement/             # App de procesos de compra
│   ├── models.py            # Solpeds, Cotizaciones, Órdenes
│   └── admin.py             # Admin de procurement
├── templates/               # Templates Jinja2
│   └── jinja2/
│       ├── base.html
│       ├── login.html
│       └── dashboard.html
├── static/                  # Archivos estáticos
├── media/                   # Archivos subidos
├── docker-compose.yml       # Configuración Docker
├── Dockerfile               # Imagen Docker
├── requirements.txt         # Dependencias Python
└── README.md               # Este archivo
```

## Modelos Principales

### Usuarios
- **Usuario**: Usuario personalizado con email como identificador

### Core
- **Proveedor**: Proveedores de productos
- **Cliente**: Clientes del sistema
- **Artículo**: Catálogo de productos
- **FormaDeEntrega**: Métodos de entrega
- **Despachante**: Empresas de envío

### Procurement
- **Solped**: Solicitud de pedido
- **PedidoDeCotizacion**: Pedido de cotización a proveedores
- **CotizacionProveedor**: Cotización recibida de proveedor
- **Cotizacion**: Cotización final al cliente
- **OrdenCompraProveedor**: Orden de compra a proveedor
- **OrdenCompraCliente**: Orden de compra del cliente
- **Remito**: Remito de entrega
- **Envio**: Seguimiento de envío
- **Actividad**: Log de auditoría

## Roles de Usuario

- **VENDEDOR**: Usuario vendedor estándar
- **COMPRADOR**: Usuario comprador
- **ADMINISTRADOR**: Acceso completo al sistema
- **SUPERVISOR**: Supervisor de operaciones

## Comandos Útiles

### Django
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Shell de Django
python manage.py shell

# Shell Plus (con django-extensions)
python manage.py shell_plus
```

### Docker
```bash
# Iniciar servicios
docker-compose up

# Iniciar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build

# Ejecutar comando en contenedor
docker-compose exec web python manage.py <comando>
```

### Celery
```bash
# Iniciar worker (local)
celery -A procurement_system worker -l info

# Iniciar beat (local)
celery -A procurement_system beat -l info

# Iniciar flower (local)
celery -A procurement_system flower --port=5555
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=.

# Tests específicos
pytest users/tests.py
```

## Variables de Entorno

Ver archivo `.env.example` para todas las variables disponibles.

Variables principales:
- `SECRET_KEY`: Clave secreta de Django
- `DEBUG`: Modo debug (True/False)
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de PostgreSQL
- `DB_PASSWORD`: Contraseña de PostgreSQL
- `REDIS_HOST`: Host de Redis
- `CELERY_BROKER_URL`: URL del broker de Celery

## Tecnologías Utilizadas

- **Backend**: Django 5.2, Python 3.11
- **Base de Datos**: PostgreSQL 16
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery 5.4
- **Frontend**: Bootstrap 5, Jinja2, Font Awesome
- **Admin**: Django Baton
- **Others**: django-allauth, django-guardian, django-money, etc.

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto es privado y propiedad de BKK.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

## Credenciales por Defecto

**Email**: admin@compras-soft.com  
**Password**: (el que definas al crear el superusuario)

## Notas Importantes

- El sistema utiliza soft delete, los registros eliminados no se borran físicamente
- Todas las operaciones importantes quedan registradas en el log de actividades
- Los índices están optimizados para búsquedas frecuentes
- Se recomienda usar PostgreSQL en producción
- Configurar correctamente las variables de entorno en producción
- Cambiar `SECRET_KEY` en producción
- Activar HTTPS en producción (`SECURE_SSL_REDIRECT=True`)

