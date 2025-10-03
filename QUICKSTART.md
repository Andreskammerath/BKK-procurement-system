# Quick Start Guide

## Getting Started with BKK Procurement System

### Option 1: Using Docker (Recommended - Easiest)

Docker will handle all dependencies, database, and services automatically.

```bash
# 1. Start all services
docker-compose up --build

# 2. In a new terminal, run migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# 3. Create a superuser
docker-compose exec web python manage.py createsuperuser

# 4. Access the application
# Login: http://localhost:8000/login/
# Admin: http://localhost:8000/admin/
# Flower: http://localhost:5555
```

That's it! The system is ready to use.

---

### Option 2: Local Development (Without Docker)

If you prefer to run locally without Docker:

#### Prerequisites
- Python 3.11+
- PostgreSQL 16+ (running locally)
- Redis 7+ (running locally)

#### Setup Steps

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and update:
# - DB_HOST=localhost (instead of 'db')
# - REDIS_HOST=localhost (instead of 'redis')

# 4. Make sure PostgreSQL is running
# Create database manually or let Django create it

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run development server
python manage.py runserver

# 9. In separate terminals, start Celery (optional):
celery -A procurement_system worker -l info
celery -A procurement_system beat -l info
celery -A procurement_system flower --port=5555
```

---

## First Login

1. Go to: http://localhost:8000/login/
2. Enter your superuser email and password
3. You'll be redirected to the dashboard

## Accessing the Admin Panel

Go to: http://localhost:8000/admin/

Here you can:
- Manage all entities (Suppliers, Clients, Articles)
- Create Solpeds, Quotations, and Purchase Orders
- View activity logs
- Manage users

---

## Common Issues

### "ModuleNotFoundError: No module named 'celery'"
**Solution**: Install dependencies first: `pip install -r requirements.txt`

### "FATAL: database does not exist"
**Solution**: 
- Using Docker: The database is created automatically
- Local: Create the database manually in PostgreSQL:
  ```sql
  CREATE DATABASE procurement_db;
  CREATE USER procurement_user WITH PASSWORD 'procurement_password';
  GRANT ALL PRIVILEGES ON DATABASE procurement_db TO procurement_user;
  ```

### "Connection refused" to PostgreSQL or Redis
**Solution**:
- Using Docker: Make sure all services are running: `docker-compose up`
- Local: Start PostgreSQL and Redis services

### Templates not found
**Solution**: Make sure `templates/jinja2/` directory exists with the HTML files

---

## Project Structure Overview

```
BKK-procurement-system/
├── users/           # User authentication & management
├── core/            # Core entities (Suppliers, Clients, Articles)
├── procurement/     # Business processes (Orders, Quotations)
├── templates/       # Jinja2 templates
├── static/          # Static files (CSS, JS, images)
├── media/           # Uploaded files
└── manage.py        # Django management script
```

---

## Next Steps

After logging in, you can:

1. **Add Suppliers**: Admin → Core → Proveedores
2. **Add Clients**: Admin → Core → Clientes
3. **Add Articles**: Admin → Core → Artículos
4. **Create Solpeds**: Admin → Procurement → Solpeds
5. **Create Quotations**: Admin → Procurement → Cotizaciones

---

## Default Credentials

When you create your superuser, you can use any email and password you want.

Recommended for testing:
- Email: `admin@compras-soft.com`
- Password: `admin123` (change this in production!)

---

## Need Help?

Check the main README.md for detailed documentation.

