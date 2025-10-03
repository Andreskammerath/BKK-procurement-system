# 🚀 START HERE - BKK Procurement System

## Quick Start (2 Minutes)

### If you have Docker installed (EASIEST):

```bash
# 1. Start everything
docker-compose up --build

# 2. Open a new terminal and run:
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# 3. Done! Visit http://localhost:8000/login/
```

### If you DON'T have Docker:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install packages
pip install -r requirements.txt

# 3. Make sure PostgreSQL and Redis are running locally

# 4. Update .env file:
# Change DB_HOST from 'db' to 'localhost'
# Change REDIS_HOST from 'redis' to 'localhost'

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Start server
python manage.py runserver

# 8. Visit http://localhost:8000/login/
```

---

## 🎯 What You Can Do Now

1. **Login** at http://localhost:8000/login/
2. **Access Admin** at http://localhost:8000/admin/
3. **Add Data**:
   - Go to Admin → Core → Proveedores (Add suppliers)
   - Go to Admin → Core → Clientes (Add clients)
   - Go to Admin → Core → Artículos (Add products)
4. **Create Business Documents**:
   - Solpeds (Purchase requests)
   - Cotizaciones (Quotations)
   - Órdenes de Compra (Purchase orders)

---

## 📖 Need More Info?

- **Quick Setup**: Read `QUICKSTART.md`
- **Full Details**: Read `README.md`
- **What Was Built**: Read `PROJECT_SUMMARY.md`

---

## ⚡ Key Features Available

- ✅ Email-based login
- ✅ 4 user roles (Vendedor, Comprador, Administrador, Supervisor)
- ✅ Complete procurement workflow
- ✅ Multi-currency support (ARS, USD, EUR, BRL)
- ✅ Beautiful admin interface (Django Baton)
- ✅ Import/Export data
- ✅ Activity logging
- ✅ Soft delete (nothing is truly deleted)

---

## 🆘 Having Issues?

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Database connection failed"
→ Make sure PostgreSQL is running
→ Or use Docker: `docker-compose up`

### "Can't find templates"
→ Templates are in `templates/jinja2/`
→ They should be there already

### Still stuck?
→ Check the detailed guides in README.md and QUICKSTART.md

---

## 🎉 You're Ready!

Your Django 5 procurement system is complete with:
- 26 models
- 3 beautiful templates
- Full authentication
- Admin interface
- Docker setup
- All from your SQL schema

**Happy coding!** 🚀

